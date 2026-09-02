# Copyright 2026 Asher Informatics PBC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Mechanism-availability record: shape invariants and the three-gate ceiling."""

import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from ashmatics_datamodels.controls import (
    AssuranceMode,
    EvidenceMechanism,
    GapCause,
    MechanismAvailability,
    MechanismAvailabilityRecord,
)

META = {
    "record_id": "t",
    "version": "0.0.1",
    "status": "draft",
    "generated": "2026-09-01",
    "scheme_ref": "ashcai:MechanismAvailabilityScheme",
    "edition_ref": "coreapp ADR-039",
    "adr_refs": ["ontology ADR-009"],
    "owner": "test",
}


def _entry(mech, ess, ent, **kw):
    e = {
        "mechanism": mech,
        "availability": {"essentials": ess, "enterprise": ent},
        "note": "test",
    }
    if ess not in ("none", "planned") or ent not in ("none", "planned"):
        e.setdefault("provided_by", ["ashmatics-coreapp"])
    e.update(kw)
    return e


def _record(**overrides):
    entries = {
        "human_assertion": _entry("human_assertion", "generally_available", "generally_available"),
        "document_submission": _entry("document_submission", "beta", "generally_available"),
        "system_query": _entry("system_query", "none", "beta"),
        "telemetry_stream": _entry("telemetry_stream", "planned", "beta"),
        "computed_derivation": _entry(
            "computed_derivation", "planned", "generally_available",
            depends_on_any=["system_query", "telemetry_stream"],
        ),
    }
    entries.update(overrides)
    return MechanismAvailabilityRecord.model_validate(
        {"record_metadata": META, "mechanisms": list(entries.values())}
    )


def test_record_must_cover_every_family():
    with pytest.raises(ValidationError, match="incomplete"):
        MechanismAvailabilityRecord.model_validate(
            {"record_metadata": META,
             "mechanisms": [_entry("human_assertion", "beta", "beta")]}
        )


def test_record_rejects_duplicate_family():
    with pytest.raises(ValidationError, match="duplicate"):
        MechanismAvailabilityRecord.model_validate(
            {"record_metadata": META,
             "mechanisms": [_entry("human_assertion", "beta", "beta")] * 2
             + [_entry(m, "none", "none") for m in
                ("document_submission", "system_query", "telemetry_stream",
                 "computed_derivation")]}
        )


def test_both_editions_required():
    with pytest.raises(ValidationError):
        _record(human_assertion={"mechanism": "human_assertion",
                                 "availability": {"enterprise": "beta"},
                                 "note": "x", "provided_by": ["ashmatics-coreapp"]})


def test_usable_state_needs_a_provider():
    with pytest.raises(ValidationError, match="provided_by is empty"):
        _record(system_query={"mechanism": "system_query",
                              "availability": {"essentials": "none", "enterprise": "beta"},
                              "note": "x"})


def test_since_only_when_usable():
    with pytest.raises(ValidationError, match="since"):
        _record(system_query=_entry("system_query", "none", "planned", since="26-R03/v0.3.0"))


def test_no_partial_and_no_free_strings():
    with pytest.raises(ValidationError):
        _record(system_query=_entry("system_query", "none", "partial"))
    with pytest.raises(ValidationError):
        _record(system_query=_entry("system_query", "none", "GA"))


def test_dependency_caps_effective_availability():
    rec = _record()
    # computed_derivation is GA on enterprise but its best upstream is beta
    assert rec.effective_availability("computed_derivation", "enterprise") is MechanismAvailability.BETA
    # on essentials both upstreams are below beta -> capped at planned
    assert rec.effective_availability("computed_derivation", "essentials") is MechanismAvailability.PLANNED


def test_platform_ceiling_per_edition():
    rec = _record()
    declared = ["human_assertion", "document_submission", "telemetry_stream"]
    assert rec.achievable_ceiling(declared, "enterprise") is AssuranceMode.COLLECTED
    # essentials: telemetry planned, document beta -> attested_with_artifact
    assert rec.achievable_ceiling(declared, "essentials") is AssuranceMode.ATTESTED_WITH_ARTIFACT
    # floor: nothing declared is still attestable
    assert rec.achievable_ceiling([], "essentials") is AssuranceMode.ATTESTED


def test_entitlement_gate_lowers_site_ceiling():
    rec = _record()
    declared = ["document_submission", "telemetry_stream"]
    no_telemetry = lambda m: m is not EvidenceMechanism.TELEMETRY_STREAM  # noqa: E731
    assert rec.achievable_ceiling(declared, "enterprise") is AssuranceMode.COLLECTED
    assert rec.achievable_ceiling(declared, "enterprise", entitled=no_telemetry) \
        is AssuranceMode.ATTESTED_WITH_ARTIFACT


def test_gap_diagnosis_resolves_to_three_meetings():
    rec = _record()
    declared = ["document_submission", "telemetry_stream"]
    # Essentials cannot reach collected -> product backlog
    assert rec.diagnose_gap("collected", declared, "essentials") is GapCause.AVAILABILITY
    # Enterprise can, but this site is not entitled -> licensing
    assert rec.diagnose_gap("collected", declared, "enterprise",
                            entitled=lambda m: m is not EvidenceMechanism.TELEMETRY_STREAM) \
        is GapCause.ENTITLEMENT
    # Enterprise, entitled -> the customer's own work
    assert rec.diagnose_gap("collected", declared, "enterprise") is GapCause.CUSTOMER
    # A reachable lower target is still the customer's work, never "none"
    assert rec.diagnose_gap("attested", declared, "essentials") is GapCause.CUSTOMER


def test_essentials_split_by_source_deployment_mode():
    rec = _record(telemetry_stream={
        "mechanism": "telemetry_stream",
        "availability": {
            "essentials": {"cloud": "beta", "hybrid": "beta", "on_premise": "none", "edge": "none"},
            "enterprise": "beta",
        },
        "provided_by": ["ashmatics-aiwatch-core"],
        "note": "hosted platform reaches cloud sources only",
    })
    declared = ["document_submission", "telemetry_stream"]
    # a cloud-hosted AI system is observable from hosted Essentials
    assert rec.achievable_ceiling(declared, "essentials", deployment_mode="cloud") is AssuranceMode.COLLECTED
    # a PACS-embedded one is not, and the gap is availability, not the customer
    assert rec.achievable_ceiling(declared, "essentials", deployment_mode="on_premise") is AssuranceMode.ATTESTED_WITH_ARTIFACT
    assert rec.diagnose_gap("collected", declared, "essentials", deployment_mode="on_premise") is GapCause.AVAILABILITY
    # unknown mode reads the weakest split value, never overstating reach
    assert rec.effective_availability("telemetry_stream", "essentials") is MechanismAvailability.NONE
    # enterprise is a single value; the mode is irrelevant there
    assert rec.achievable_ceiling(declared, "enterprise", deployment_mode="on_premise") is AssuranceMode.COLLECTED


def test_split_requires_all_four_modes():
    with pytest.raises(ValidationError):
        _record(telemetry_stream={
            "mechanism": "telemetry_stream",
            "availability": {"essentials": {"cloud": "beta"}, "enterprise": "beta"},
            "provided_by": ["ashmatics-aiwatch-core"], "note": "x",
        })


def test_draft_record_is_not_confirmed():
    assert _record().is_confirmed is False


def test_minimum_availability_is_a_dial():
    rec = _record()
    declared = ["telemetry_stream"]
    assert rec.achievable_ceiling(declared, "enterprise") is AssuranceMode.COLLECTED
    assert rec.achievable_ceiling(
        declared, "enterprise", minimum=MechanismAvailability.GENERALLY_AVAILABLE
    ) is AssuranceMode.ATTESTED


# --- the live seed record in asher-infra ------------------------------------

def _seed_path() -> Path | None:
    env = os.environ.get("ASHER_INFRA_DIR")
    root = Path(env).expanduser() if env else Path(__file__).resolve().parents[2].parent / "asher-infra"
    p = root / "platform-capabilities" / "mechanism-availability.yaml"
    return p if p.is_file() else None


@pytest.mark.skipif(_seed_path() is None, reason="asher-infra seed record not checked out beside this repo")
def test_seed_record_validates_and_round_trips():
    yaml = pytest.importorskip("yaml")
    raw = yaml.safe_load(_seed_path().read_text())
    rec = MechanismAvailabilityRecord.model_validate(raw)
    # Lossless: re-validating the dump yields an equal model, and no field in
    # the file was silently dropped (extra="forbid" guarantees none was ignored).
    again = MechanismAvailabilityRecord.model_validate(rec.model_dump(mode="json"))
    assert again == rec
    assert {e.mechanism for e in rec.mechanisms} == {m.value for m in EvidenceMechanism}
    assert rec.record_metadata.status in {"draft", "confirmed", "superseded"}
    # The seed's own claim about itself, which coreapp will read first:
    assert rec.achievable_ceiling(
        ["human_assertion", "document_submission", "system_query",
         "telemetry_stream", "computed_derivation"], "enterprise",
    ) is not None
