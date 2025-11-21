# Copyright 2025 Asher Informatics PBC
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
Clinical AI Use Case taxonomy and schemas.

Provides hierarchical categorization for clinical AI applications,
including specialty, modality, and clinical context classification.
"""

from ashmatics_datamodels.use_cases.categories import (
    UseCaseCategoryBase,
    UseCaseCategoryCreate,
    UseCaseCategoryResponse,
    UseCaseCategoryTree,
)
from ashmatics_datamodels.use_cases.enums import (
    ClinicalDomain,
    ClinicalSpecialty,
    DeploymentModel,
    EvidenceStrength,
    IntegrationTarget,
)
from ashmatics_datamodels.use_cases.use_cases import (
    UseCaseBase,
    UseCaseCreate,
    UseCaseResponse,
)

__all__ = [
    # Enums
    "ClinicalDomain",
    "ClinicalSpecialty",
    "DeploymentModel",
    "IntegrationTarget",
    "EvidenceStrength",
    # Categories
    "UseCaseCategoryBase",
    "UseCaseCategoryCreate",
    "UseCaseCategoryResponse",
    "UseCaseCategoryTree",
    # Use Cases
    "UseCaseBase",
    "UseCaseCreate",
    "UseCaseResponse",
]
