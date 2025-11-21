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
Clinical AI Use Case schemas.

Core schemas for representing clinical AI use cases including
clinical context, technical requirements, and evidence mapping.
"""

from typing import Optional

from pydantic import Field

from ashmatics_datamodels.common.base import AshMaticsBaseModel, AuditedModel
from ashmatics_datamodels.fda.enums import Modality
from ashmatics_datamodels.use_cases.enums import (
    ClinicalDomain,
    ClinicalSpecialty,
    DeploymentModel,
    EvidenceStrength,
    IntegrationTarget,
    UseCaseStatus,
)


class ApplicableProduct(AshMaticsBaseModel):
    """Reference to an FDA-cleared product applicable to this use case."""

    product_id: Optional[str] = Field(None, description="Internal product ID")
    product_name: str = Field(..., max_length=255, description="Product name")
    manufacturer: Optional[str] = Field(None, max_length=255, description="Manufacturer name")
    k_number: Optional[str] = Field(None, description="FDA 510(k) number if cleared")


class SupportingEvidence(AshMaticsBaseModel):
    """Reference to clinical evidence supporting this use case."""

    evidence_id: Optional[str] = Field(None, description="Internal evidence ID")
    title: str = Field(..., max_length=500, description="Study/publication title")
    evidence_strength: Optional[EvidenceStrength] = Field(
        None, description="Strength of evidence"
    )
    findings_summary: Optional[str] = Field(
        None, description="Summary of key findings"
    )
    doi: Optional[str] = Field(None, description="DOI if published")


class TechnicalRequirements(AshMaticsBaseModel):
    """Technical requirements for implementing a use case."""

    imaging_modality: Optional[Modality] = Field(
        None, description="Primary imaging modality"
    )
    image_characteristics: Optional[str] = Field(
        None, description="Required image characteristics (e.g., 'PA and AP chest radiographs')"
    )
    integration_targets: Optional[list[IntegrationTarget]] = Field(
        None, description="Systems requiring integration"
    )
    deployment_model: Optional[DeploymentModel] = Field(
        None, description="Deployment model"
    )
    minimum_requirements: Optional[str] = Field(
        None, description="Minimum technical requirements"
    )


class ClinicalContext(AshMaticsBaseModel):
    """Clinical context and workflow information for a use case."""

    workflow_description: Optional[str] = Field(
        None, description="Description of clinical workflow"
    )
    pain_points: Optional[list[str]] = Field(
        None, description="Clinical pain points addressed"
    )
    value_proposition: Optional[str] = Field(
        None, description="Value proposition for adopting AI solution"
    )
    target_users: Optional[list[str]] = Field(
        None, description="Primary users (e.g., 'Radiologist', 'Emergency Physician')"
    )


class UseCaseBase(AshMaticsBaseModel):
    """
    Base schema for clinical AI use cases.

    Represents a specific clinical scenario where AI can be applied,
    including context, requirements, and evidence mapping.
    """

    # Basic identification
    title: str = Field(
        ..., max_length=255, description="Use case title"
    )
    description: Optional[str] = Field(
        None, description="Detailed use case description"
    )

    # Classification
    clinical_domain: ClinicalDomain = Field(
        ..., description="Primary clinical domain"
    )
    clinical_specialty: Optional[ClinicalSpecialty] = Field(
        None, description="Specific clinical specialty"
    )
    anatomical_region: Optional[str] = Field(
        None, max_length=100, description="Anatomical region (e.g., 'chest', 'brain')"
    )
    pathology: Optional[list[str]] = Field(
        None, description="Target pathologies (e.g., ['pneumonia', 'pleural_effusion'])"
    )

    # Categorization
    category_ids: Optional[list[int]] = Field(
        None, description="Associated use case category IDs"
    )
    tags: Optional[list[str]] = Field(
        None, description="Searchable tags"
    )

    # Status
    status: Optional[UseCaseStatus] = Field(
        UseCaseStatus.DRAFT, description="Curation status"
    )


class UseCaseCreate(UseCaseBase):
    """Schema for creating a new use case."""

    # Clinical context (optional at creation)
    clinical_context: Optional[ClinicalContext] = None

    # Technical requirements (optional at creation)
    technical_requirements: Optional[TechnicalRequirements] = None


class UseCaseResponse(UseCaseBase, AuditedModel):
    """
    Full use case response with all details.

    Includes clinical context, technical requirements, applicable products,
    and supporting evidence.
    """

    id: Optional[str] = Field(None, description="Use case ID")

    # Clinical context
    clinical_context: Optional[ClinicalContext] = Field(
        None, description="Clinical workflow context"
    )

    # Technical requirements
    technical_requirements: Optional[TechnicalRequirements] = Field(
        None, description="Technical implementation requirements"
    )

    # Related products
    applicable_products: Optional[list[ApplicableProduct]] = Field(
        None, description="FDA-cleared products applicable to this use case"
    )

    # Evidence
    supporting_evidence: Optional[list[SupportingEvidence]] = Field(
        None, description="Clinical evidence supporting this use case"
    )

    # Implementation guidance
    implementation_considerations: Optional[str] = Field(
        None, description="Key considerations for implementation"
    )
    regulatory_considerations: Optional[str] = Field(
        None, description="Regulatory considerations"
    )
