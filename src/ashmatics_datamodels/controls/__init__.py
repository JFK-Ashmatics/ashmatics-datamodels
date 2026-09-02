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
CHAR controls-catalog contracts (ontology ADR-009; aigov-framework
Control-Maturity-Schema-Proposal).

The five control axes as ontology-bound enums, and the platform
mechanism-availability record with the three-gate assurance ceiling::

    from ashmatics_datamodels.controls import (
        AssuranceMode, EvidenceMechanism, MechanismAvailability, Edition,
        MechanismAvailabilityRecord, GapCause,
    )

    rec = MechanismAvailabilityRecord.model_validate(yaml.safe_load(f))
    rec.achievable_ceiling(["document_submission", "telemetry_stream"], "enterprise")
    rec.achievable_ceiling(declared, "essentials", deployment_mode=system.deployment_mode)
    rec.diagnose_gap("collected", declared, "enterprise", entitled=site.may_use)

The catalog and profile document contracts (the equivalent of
``MethodRegistry`` for ``ashc_controls_catalog.yaml``) are the queued
follow-up; this module ships the axis vocabularies they will share.
"""

from .availability import (
    COMPONENT_TOKEN_PATTERN,
    DEFAULT_MINIMUM_AVAILABILITY,
    AvailabilityRecordMetadata,
    ByDeploymentMode,
    EditionAvailability,
    GapCause,
    MechanismAvailabilityEntry,
    MechanismAvailabilityRecord,
)
from .enums import (
    ASSURANCE_ORDINAL,
    AVAILABILITY_ORDINAL,
    CADENCE_ORDINAL,
    MATURITY_ORDINAL,
    YIELDS_ASSURANCE_MODE,
    AssuranceCadence,
    AssuranceMode,
    ControlMaturity,
    DeploymentMode,
    Edition,
    EvidenceMechanism,
    MechanismAvailability,
)

__all__ = [
    "ASSURANCE_ORDINAL",
    "AVAILABILITY_ORDINAL",
    "CADENCE_ORDINAL",
    "COMPONENT_TOKEN_PATTERN",
    "DEFAULT_MINIMUM_AVAILABILITY",
    "MATURITY_ORDINAL",
    "YIELDS_ASSURANCE_MODE",
    "AssuranceCadence",
    "AssuranceMode",
    "AvailabilityRecordMetadata",
    "ByDeploymentMode",
    "ControlMaturity",
    "DeploymentMode",
    "Edition",
    "EditionAvailability",
    "EvidenceMechanism",
    "GapCause",
    "MechanismAvailability",
    "MechanismAvailabilityEntry",
    "MechanismAvailabilityRecord",
]
