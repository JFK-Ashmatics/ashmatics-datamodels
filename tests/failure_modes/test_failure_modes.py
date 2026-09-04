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

"""Contract tests for the CHAR failure mode taxonomy models (ASHFORGE-604)."""

import pytest
from pydantic import ValidationError

from ashmatics_datamodels.failure_modes import (
    ActionAuthority,
    AIFailureMode,
    FailureModeApplicability,
    FailureModeDefinition,
    FailureModeTaxonomy,
    Repercussion,
    RepercussionAudience,
)


def _definition(**overrides) -> dict:
    base = {
        "failure_mode": AIFailureMode.SILENT_DEGRADATION,
        "label": "Silent performance degradation",
        "description": "Accuracy falls while output stays plausible.",
        "what_it_looks_like": ["Outputs remain well-formed as accuracy falls."],
        "repercussions": [
            {
                "audience": RepercussionAudience.OPERATOR,
                "clinical": "Nothing about the output announces the drop.",
            }
        ],
        "junction_refs": ["SOP-RM-01.S3"],
    }
    base.update(overrides)
    return base


def test_minimal_definition_validates():
    fm = FailureModeDefinition(**_definition())
    # use_enum_values=True on the repo base model: the field holds the value
    assert fm.failure_mode == AIFailureMode.SILENT_DEGRADATION.value
    # applicability defaults to unrestricted on every axis
    assert fm.applicability.ai_paradigm is None
    assert fm.detectable_by == []


def test_label_may_not_repeat_the_id():
    with pytest.raises(ValidationError, match="human-readable name"):
        FailureModeDefinition(**_definition(label="fm-silent-degradation"))


def test_repercussion_needs_a_framing():
    """An audience with neither framing says nothing and must not validate."""
    with pytest.raises(ValidationError, match="clinical or a non-clinical"):
        Repercussion(audience=RepercussionAudience.AFFECTED_PERSON)


def test_repercussion_accepts_non_clinical_only():
    """Non-clinical AI is in scope: an administrative system fails differently
    and the repercussion is not patient harm."""
    r = Repercussion(
        audience=RepercussionAudience.ORGANIZATION,
        non_clinical="Scheduling capacity is misallocated for a full cycle.",
    )
    assert r.clinical is None


def test_what_it_looks_like_is_required():
    """The difference between a taxonomy and a word list."""
    with pytest.raises(ValidationError):
        FailureModeDefinition(**_definition(what_it_looks_like=[]))


def test_junction_ref_pattern_is_enforced():
    with pytest.raises(ValidationError):
        FailureModeDefinition(**_definition(junction_refs=["hazard analysis"]))


def test_applicability_rejects_free_strings():
    """ADR-011's zero-free-string criterion, carried over."""
    with pytest.raises(ValidationError):
        FailureModeApplicability(ai_paradigm=["generative"])


def test_applicability_accepts_action_authority():
    ap = FailureModeApplicability(
        action_authority=[ActionAuthority.ACT_AUTONOMOUSLY]
    )
    assert ap.action_authority == [ActionAuthority.ACT_AUTONOMOUSLY.value]


def test_duplicate_failure_modes_rejected():
    meta = {
        "taxonomy_id": "char-failure-mode-taxonomy",
        "version": "0.1.0",
        "status": "pilot",
        "scope": "RM hazard analysis, surveillance and incident triage",
        "created": "2026-09-04",
        "last_updated": "2026-09-04",
        "review_cycle": "annual",
    }
    with pytest.raises(ValidationError, match="duplicate failure_mode"):
        FailureModeTaxonomy(
            taxonomy_metadata=meta,
            failure_modes=[_definition(), _definition()],
        )


def test_enum_covers_ten_classes():
    """Guards against a class being dropped silently; the ontology-side
    completeness check lives in test_ontology_binding."""
    assert len(list(AIFailureMode)) == 10
