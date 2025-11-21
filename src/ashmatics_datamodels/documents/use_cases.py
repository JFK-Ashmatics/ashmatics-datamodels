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
Use Case schemas for kb_use_cases collection.

Clinical use cases with workflow context, technical requirements,
applicable products, and supporting evidence.

Reference: docs/Plans/DocumentDataModelSchema-Normalize-2025-11-15/
"""

from typing import Optional

from pydantic import Field

from ashmatics_datamodels.common.base import AshMaticsBaseModel
from ashmatics_datamodels.documents.base import (
    ContentBase,
    ContentType,
    DocumentSummaryBase,
    DocumentType,
    MetadataContentBase,
    MetadataObjectBase,
    MongoDocumentBase,
    SectionBase,
)


# =============================================================================
# Use Case Nested Schemas
# =============================================================================


class ApplicableProductRef(AshMaticsBaseModel):
    """Reference to an applicable product."""

    product_id: Optional[str] = Field(
        None,
        description="Reference to kb_product_cards document",
    )
    product_name: str = Field(
        ...,
        description="Product name",
    )
    manufacturer: Optional[str] = Field(
        None,
        description="Manufacturer name",
    )
    k_number: Optional[str] = Field(
        None,
        description="510(k) number if cleared",
    )


class SupportingEvidenceRef(AshMaticsBaseModel):
    """Reference to supporting evidence."""

    evidence_id: Optional[str] = Field(
        None,
        description="Reference to kb_evidence_docs document",
    )
    title: str = Field(
        ...,
        description="Evidence title",
    )
    evidence_strength: Optional[str] = Field(
        None,
        description="Evidence strength (e.g., 'strong', 'moderate', 'limited')",
    )
    findings_summary: Optional[str] = Field(
        None,
        description="Summary of key findings",
    )


# =============================================================================
# Use Case Sections
# =============================================================================


class UseCaseOverviewSection(SectionBase):
    """Use case overview section."""

    title: str = Field(default="Use Case Overview", description="Section title")
    order: int = Field(default=1, description="Section order")
    description: Optional[str] = Field(
        None,
        description="Use case description",
    )


class ClinicalContextSection(SectionBase):
    """Clinical context section."""

    title: str = Field(default="Clinical Context", description="Section title")
    order: int = Field(default=2, description="Section order")
    workflow: Optional[str] = Field(
        None,
        description="Clinical workflow description",
    )
    pain_points: list[str] = Field(
        default_factory=list,
        description="Current pain points addressed",
    )
    value_proposition: Optional[str] = Field(
        None,
        description="Value proposition of AI solution",
    )


class TechnicalRequirementsSection(SectionBase):
    """Technical requirements section."""

    title: str = Field(default="Technical Requirements", description="Section title")
    order: int = Field(default=3, description="Section order")
    imaging_modality: Optional[str] = Field(
        None,
        description="Required imaging modality",
    )
    image_characteristics: Optional[str] = Field(
        None,
        description="Required image characteristics",
    )
    integration_needs: list[str] = Field(
        default_factory=list,
        description="Integration requirements (e.g., ['PACS', 'EMR'])",
    )


class ApplicableProductsSection(SectionBase):
    """Applicable products section."""

    title: str = Field(default="Applicable Products", description="Section title")
    order: int = Field(default=4, description="Section order")
    fda_cleared_products: list[ApplicableProductRef] = Field(
        default_factory=list,
        description="FDA-cleared products for this use case",
    )


class SupportingEvidenceSection(SectionBase):
    """Supporting evidence section."""

    title: str = Field(default="Clinical Evidence", description="Section title")
    order: int = Field(default=5, description="Section order")
    key_studies: list[SupportingEvidenceRef] = Field(
        default_factory=list,
        description="Key supporting studies",
    )


class ImplementationSection(SectionBase):
    """Implementation considerations section."""

    title: str = Field(default="Implementation", description="Section title")
    order: int = Field(default=6, description="Section order")
    deployment_model: Optional[str] = Field(
        None,
        description="Recommended deployment model",
    )
    training_requirements: Optional[str] = Field(
        None,
        description="User training requirements",
    )
    regulatory_considerations: Optional[str] = Field(
        None,
        description="Regulatory considerations",
    )


# =============================================================================
# Use Case Metadata Content
# =============================================================================


class UseCaseMetadataContent(MetadataContentBase):
    """
    Metadata content specific to use cases.
    """

    document_type: DocumentType = Field(
        default=DocumentType.USE_CASE,
        description="Always 'kb_use_case'",
    )
    content_type: ContentType = Field(
        default=ContentType.CLINICAL_USE_CASE,
        description="Clinical use case type",
    )

    # Use case identification
    clinical_specialty: Optional[str] = Field(
        None,
        description="Clinical specialty (e.g., 'Emergency Medicine')",
    )
    anatomical_region: Optional[str] = Field(
        None,
        description="Anatomical region (e.g., 'chest')",
    )
    pathology: list[str] = Field(
        default_factory=list,
        description="Target pathologies",
    )


# =============================================================================
# Use Case Content
# =============================================================================


class UseCaseContent(ContentBase):
    """
    Content structure for use cases.
    """

    sections: dict[str, SectionBase] = Field(
        default_factory=lambda: {
            "use_case_overview": UseCaseOverviewSection(
                title="Use Case Overview", order=1
            ),
            "clinical_context": ClinicalContextSection(
                title="Clinical Context", order=2
            ),
            "technical_requirements": TechnicalRequirementsSection(
                title="Technical Requirements", order=3
            ),
            "applicable_products": ApplicableProductsSection(
                title="Applicable Products", order=4
            ),
            "supporting_evidence": SupportingEvidenceSection(
                title="Clinical Evidence", order=5
            ),
            "implementation_considerations": ImplementationSection(
                title="Implementation", order=6
            ),
        },
        description="Use case sections",
    )


# =============================================================================
# Complete Use Case Document
# =============================================================================


class UseCaseDocument(MongoDocumentBase):
    """
    Complete use case with three-tier structure.

    Used for kb_use_cases MongoDB collection.
    """

    metadata_object: MetadataObjectBase = Field(
        default_factory=MetadataObjectBase,
        description="Artifact metadata",
    )
    metadata_content: UseCaseMetadataContent = Field(
        ...,
        description="Use case metadata",
    )
    content: UseCaseContent = Field(
        default_factory=UseCaseContent,
        description="Use case content",
    )


class UseCaseDocumentCreate(MongoDocumentBase):
    """Schema for creating a new use case."""

    metadata_content: UseCaseMetadataContent = Field(
        ...,
        description="Required use case metadata",
    )
    content: UseCaseContent = Field(
        default_factory=UseCaseContent,
        description="Use case content",
    )


# =============================================================================
# Use Case Summary
# =============================================================================


class UseCaseSummary(DocumentSummaryBase):
    """
    Summary view for use cases in listings.
    """

    document_type: DocumentType = Field(
        default=DocumentType.USE_CASE,
        description="Always kb_use_case",
    )

    # Use case-specific summary fields
    clinical_specialty: Optional[str] = Field(
        None,
        description="Clinical specialty",
    )
    anatomical_region: Optional[str] = Field(
        None,
        description="Anatomical region",
    )
    pathology: list[str] = Field(
        default_factory=list,
        description="Target pathologies",
    )

    @classmethod
    def from_document(cls, doc: UseCaseDocument) -> "UseCaseSummary":
        """Create summary from full use case."""
        return cls(
            _id=doc.id or "",
            document_type=doc.metadata_content.document_type,
            content_type=doc.metadata_content.content_type,
            title=doc.metadata_content.title,
            clinical_domain=doc.metadata_content.clinical_domain,
            tags=doc.metadata_content.tags,
            created_at=doc.metadata_object.created_at,
            updated_at=doc.metadata_object.updated_at,
            clinical_specialty=doc.metadata_content.clinical_specialty,
            anatomical_region=doc.metadata_content.anatomical_region,
            pathology=doc.metadata_content.pathology,
        )
