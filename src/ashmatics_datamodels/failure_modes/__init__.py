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
CHAR AI failure mode taxonomy contracts (aigov-framework ASHFORGE-604,
ADR-018 D3).

How a governed AI system fails, and what follows from that failure. Reference
content resolved at SOP junctions — consulted by RM.BP01 hazard analysis,
RM.BP04 post-deployment surveillance and RM.BP05 incident triage — not a base
practice and not a method.

    from ashmatics_datamodels.failure_modes import (
        AIFailureMode,
        FailureModeTaxonomy,
        FailureModeDefinition,
        FailureModeApplicability,
        Repercussion,
    )
"""

from .enums import ActionAuthority, AIFailureMode, RepercussionAudience
from .taxonomy import (
    FailureModeApplicability,
    FailureModeDefinition,
    FailureModeTaxonomy,
    Repercussion,
    TaxonomyMetadata,
)

__all__ = [
    "ActionAuthority",
    "AIFailureMode",
    "RepercussionAudience",
    "FailureModeApplicability",
    "FailureModeDefinition",
    "FailureModeTaxonomy",
    "Repercussion",
    "TaxonomyMetadata",
]
