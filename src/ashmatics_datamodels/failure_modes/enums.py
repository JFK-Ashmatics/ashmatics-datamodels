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
AI failure-mode vocabulary for the CHAR failure mode taxonomy.

Single source of truth for the failure classes shared by the aigov-framework
taxonomy registry (``failure_mode_taxonomy.yaml``) and anything downstream that
reasons over how a governed system fails. Authored per aigov-framework ADR-018
D3 (the taxonomy is a registry asset resolved at SOP junctions, following the
ADR-011 method registry pattern — not a base practice and not a work product).

Ontology binding follows the ADR-002 convention: ``x_ontology_scheme`` is
asserted on the model fields that use these enums (``taxonomy.py``), and the CI
guard (``tests/failure_modes/test_ontology_binding.py``) checks every member
resolves in its scheme in ``ashmatics-unified-ontology.ttl``.

Value convention matches the methods module: ontology concept LOCAL NAMES
(``fm-silent-degradation``), which are the canonical CHAR concept IDs used in
the taxonomy registry. The concepts' ``skos:notation`` values differ
(``"silent_degradation"``) and the binding guard accepts either.

WHAT IS NOT A FAILURE MODE. A hazard is harm reaching a person; a failure mode
is the system behaviour that can lead there, and several classes below reach no
patient at all in an administrative system. A THREAT is a failure reached on
purpose by an adversary — CHAR assesses those under RM.BP03 and ASHC-SEC-02, not
here; see ``OUT_OF_DISTRIBUTION_INPUT``.
"""

from enum import Enum

# ActionAuthority moved to common/enums.py in 0.15.0: it is a SYSTEM facet
# (ash:ActionAuthorityScheme), not a failure-mode concept, and it landed here
# only because failure-mode applicability was the first thing to need it.
# Method applicability now needs it too. Re-exported so existing imports from
# this module keep working.
from ..common.enums import ActionAuthority as ActionAuthority  # noqa: F401


class AIFailureMode(str, Enum):
    """``ash:AIFailureModeScheme`` — how an AI system stops performing as intended."""

    DISTRIBUTIONAL_SHIFT = "fm-distributional-shift"
    SILENT_DEGRADATION = "fm-silent-degradation"
    CALIBRATION_DRIFT = "fm-calibration-drift"
    AUTOMATION_BIAS = "fm-automation-bias"
    ALERT_FATIGUE = "fm-alert-fatigue"
    CONFABULATION = "fm-confabulation"
    # Incidental only. Deliberately crafted input reaching the same mechanism is a
    # threat, assessed under RM.BP03 / ASHC-SEC-02 rather than as a failure mode.
    OUT_OF_DISTRIBUTION_INPUT = "fm-out-of-distribution-input"
    FEEDBACK_LOOP = "fm-feedback-loop"
    UPSTREAM_DATA_FAILURE = "fm-upstream-data-failure"
    SILENT_INCOMPETENCE = "fm-silent-incompetence"


class RepercussionAudience(str, Enum):
    """
    Who experiences a failure. Not an ontology scheme: this is the shape of the
    taxonomy's repercussion half, not a classification of systems.

    The two audiences are deliberately separate. A failure that a clinician sees
    immediately and a patient never experiences is a different governance problem
    from one a patient experiences and no operator ever sees.
    """

    OPERATOR = "operator"
    AFFECTED_PERSON = "affected_person"
    ORGANIZATION = "organization"
