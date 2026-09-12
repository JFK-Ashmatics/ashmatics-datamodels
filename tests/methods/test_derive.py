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

"""
Per-member provenance derivation (ADR-022 D6).

The contract these tests hold: provenance is a VIEW over `members` and
`adjustments`, never a stored field, so there is no second answer to
disagree with the first. The last test is the counterpart of 0.12.0's
system_class parity test — it asserts the derivation and the underlying
written facts cannot diverge, because there is only one written fact.
"""

import pytest

from ashmatics_datamodels.methods import (
    ApprovedMethodSet,
    MemberProvenance,
    member_provenance,
)

EXEMPLAR = "mth://fairness.subgroup_auroc"
ADJUDICATED = "mth://fairness.calibration_by_group"
OTHER = "mth://fairness.demographic_parity"

BASE = {
    "set_id": "mset://fairness.core",
    "label": "Core set",
    "description": "The single org-approved fairness set.",
    "serves_junctions": [
        {"ref": "SOP-EF-01.S1", "phase": "validation", "note": "primary"}
    ],
    "members": {"validation": [EXEMPLAR]},
    "token": "{{efApprovedFairnessMethods}}",
    "organization_id": "org-001",
    "delivery_mode": "align",
}


def _approved(**over) -> ApprovedMethodSet:
    return ApprovedMethodSet.model_validate({**BASE, **over})


def test_baseline_member_is_an_asher_exemplar():
    got = member_provenance(_approved(resolved_members={"validation": [EXEMPLAR]}))
    assert got == {"validation": {EXEMPLAR: MemberProvenance.ASHER_EXEMPLAR}}


def test_added_member_is_organizationally_adjudicated():
    got = member_provenance(
        _approved(
            resolved_members={"validation": [EXEMPLAR, ADJUDICATED]},
            adjustments=[
                {
                    "action": "added",
                    "method_id": ADJUDICATED,
                    "phase": "validation",
                    "rationale": "local prevalence differs",
                }
            ],
        )
    )
    assert got["validation"] == {
        EXEMPLAR: MemberProvenance.ASHER_EXEMPLAR,
        ADJUDICATED: MemberProvenance.ORGANIZATIONALLY_ADJUDICATED,
    }


def test_phase_both_adjustment_covers_both_concrete_phases():
    """
    The trap: resolved_members is keyed only by the two concrete phases,
    but an adjustment may carry phase 'both'. Read naively, a member added
    for both phases reads as an exemplar under whichever phase it was not
    literally matched against.
    """
    got = member_provenance(
        _approved(
            members={"validation": [EXEMPLAR], "operational": [EXEMPLAR]},
            resolved_members={
                "validation": [ADJUDICATED],
                "operational": [ADJUDICATED],
            },
            adjustments=[
                {
                    "action": "added",
                    "method_id": ADJUDICATED,
                    "phase": "both",
                    "rationale": "needed in both phases",
                }
            ],
        )
    )
    assert got["validation"][ADJUDICATED] is (
        MemberProvenance.ORGANIZATIONALLY_ADJUDICATED
    )
    assert got["operational"][ADJUDICATED] is (
        MemberProvenance.ORGANIZATIONALLY_ADJUDICATED
    )


@pytest.mark.parametrize("action", ["removed", "reranked"])
def test_only_added_confers_adjudicated_provenance(action):
    """
    `reranked` changes order and leaves a member whatever it already was;
    `removed` members are not in resolved_members at all. Neither is an
    origin, so a member present only via one of them is unattributable.
    """
    with pytest.raises(ValueError, match="provenance cannot be established"):
        member_provenance(
            _approved(
                resolved_members={"validation": [EXEMPLAR, OTHER]},
                adjustments=[
                    {
                        "action": action,
                        "method_id": OTHER,
                        "phase": "validation",
                        "rationale": "ranked below the primary",
                    }
                ],
            )
        )


def test_unattributable_member_raises_rather_than_defaulting():
    """
    Fail loudly, like the registry derivations. A silent default would make
    an unattributable member indistinguishable from a warranted one, which
    is precisely the confusion ADR-022 D6 exists to prevent.
    """
    with pytest.raises(ValueError, match=r"neither the exemplar baseline"):
        member_provenance(_approved(resolved_members={"validation": [OTHER]}))


def test_baseline_wins_when_a_member_is_both():
    """A re-added exemplar still came from Asher; the warrant is unchanged."""
    got = member_provenance(
        _approved(
            resolved_members={"validation": [EXEMPLAR]},
            adjustments=[
                {
                    "action": "added",
                    "method_id": EXEMPLAR,
                    "phase": "validation",
                    "rationale": "re-affirmed after review",
                }
            ],
        )
    )
    assert got["validation"][EXEMPLAR] is MemberProvenance.ASHER_EXEMPLAR


def test_provenance_is_a_view_not_a_second_stored_answer():
    """
    The parity guarantee, held structurally: ApprovedMethodSet has no
    provenance field, so there is nothing for the derivation to disagree
    with. If someone adds one, this fails and they must read ADR-022 D6 and
    the 0.12.0 system_class entry before proceeding.
    """
    fields = set(ApprovedMethodSet.model_fields)
    assert not {f for f in fields if "provenance" in f or "origin" in f}


def test_operator_selected_is_not_a_value_here():
    """
    ADR-022 D6 names three origins; this enum has two. The third is
    recorded against the job in the customer's datastore under D5 and is
    never claimed by CHAR, so it cannot occur in an org's standing approved
    set. Adding it here would mint a value nothing can produce.
    """
    assert {m.value for m in MemberProvenance} == {
        "asher_exemplar",
        "organizationally_adjudicated",
    }
