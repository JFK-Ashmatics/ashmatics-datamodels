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
Manufacturer Card schemas for kb_manufacturer_cards collection.

Company profiles with product portfolio, regulatory history,
and research partnerships.

Reference: docs/Plans/DocumentDataModelSchema-Normalize-2025-11-15/
"""

from datetime import date
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
# Manufacturer Card Nested Schemas
# =============================================================================


class ProductRef(AshMaticsBaseModel):
    """Reference to a product in portfolio."""

    product_id: Optional[str] = Field(
        None,
        description="Reference to kb_product_cards document",
    )
    product_name: str = Field(
        ...,
        description="Product name",
    )
    clinical_domain: Optional[str] = Field(
        None,
        description="Clinical domain",
    )
    fda_status: Optional[str] = Field(
        None,
        description="FDA status",
    )


class ClearanceRef(AshMaticsBaseModel):
    """Reference to an FDA clearance."""

    k_number: str = Field(
        ...,
        description="510(k) number",
    )
    product: Optional[str] = Field(
        None,
        description="Product name",
    )
    clearance_date: Optional[date] = Field(
        None,
        description="Clearance date",
    )


# =============================================================================
# Manufacturer Card Sections
# =============================================================================


class CompanyOverviewSection(SectionBase):
    """Company overview section."""

    title: str = Field(default="Company Overview", description="Section title")
    order: int = Field(default=1, description="Section order")
    description: Optional[str] = Field(
        None,
        description="Company description",
    )
    employee_count: Optional[int] = Field(
        None,
        ge=0,
        description="Number of employees",
    )
    funding_stage: Optional[str] = Field(
        None,
        description="Funding stage (e.g., 'Series A', 'Series C', 'Public')",
    )


class ProductPortfolioSection(SectionBase):
    """Product portfolio section."""

    title: str = Field(default="Product Portfolio", description="Section title")
    order: int = Field(default=2, description="Section order")
    products: list[ProductRef] = Field(
        default_factory=list,
        description="Products in portfolio",
    )


class RegulatoryHistorySection(SectionBase):
    """Regulatory history section."""

    title: str = Field(default="Regulatory History", description="Section title")
    order: int = Field(default=3, description="Section order")
    fda_clearances: list[ClearanceRef] = Field(
        default_factory=list,
        description="FDA clearances received",
    )


class ResearchPartnershipsSection(SectionBase):
    """Research partnerships section."""

    title: str = Field(default="Research & Partnerships", description="Section title")
    order: int = Field(default=4, description="Section order")
    academic_collaborations: list[str] = Field(
        default_factory=list,
        description="Academic collaboration partners",
    )
    industry_partners: list[str] = Field(
        default_factory=list,
        description="Industry partners",
    )


# =============================================================================
# Manufacturer Card Metadata Content
# =============================================================================


class ManufacturerCardMetadataContent(MetadataContentBase):
    """
    Metadata content specific to manufacturer cards.
    """

    document_type: DocumentType = Field(
        default=DocumentType.MANUFACTURER_CARD,
        description="Always 'kb_manufacturer_card'",
    )
    content_type: ContentType = Field(
        default=ContentType.COMPANY_PROFILE,
        description="Company profile type",
    )

    # Company identification
    company_name: str = Field(
        ...,
        description="Company name",
    )
    headquarters: Optional[str] = Field(
        None,
        description="Headquarters location",
    )
    founded: Optional[str] = Field(
        None,
        description="Year founded",
    )
    website: Optional[str] = Field(
        None,
        description="Company website URL",
    )


# =============================================================================
# Manufacturer Card Content
# =============================================================================


class ManufacturerCardContent(ContentBase):
    """
    Content structure for manufacturer cards.
    """

    sections: dict[str, SectionBase] = Field(
        default_factory=lambda: {
            "company_overview": CompanyOverviewSection(
                title="Company Overview", order=1
            ),
            "product_portfolio": ProductPortfolioSection(
                title="Product Portfolio", order=2
            ),
            "regulatory_history": RegulatoryHistorySection(
                title="Regulatory History", order=3
            ),
            "research_partnerships": ResearchPartnershipsSection(
                title="Research & Partnerships", order=4
            ),
        },
        description="Manufacturer card sections",
    )


# =============================================================================
# Complete Manufacturer Card Document
# =============================================================================


class ManufacturerCardDocument(MongoDocumentBase):
    """
    Complete manufacturer card with three-tier structure.

    Used for kb_manufacturer_cards MongoDB collection.
    """

    metadata_object: MetadataObjectBase = Field(
        default_factory=MetadataObjectBase,
        description="Artifact metadata",
    )
    metadata_content: ManufacturerCardMetadataContent = Field(
        ...,
        description="Manufacturer card metadata",
    )
    content: ManufacturerCardContent = Field(
        default_factory=ManufacturerCardContent,
        description="Manufacturer card content",
    )


class ManufacturerCardDocumentCreate(MongoDocumentBase):
    """Schema for creating a new manufacturer card."""

    metadata_content: ManufacturerCardMetadataContent = Field(
        ...,
        description="Required manufacturer card metadata",
    )
    content: ManufacturerCardContent = Field(
        default_factory=ManufacturerCardContent,
        description="Manufacturer card content",
    )


# =============================================================================
# Manufacturer Card Summary
# =============================================================================


class ManufacturerCardSummary(DocumentSummaryBase):
    """
    Summary view for manufacturer cards in listings.
    """

    document_type: DocumentType = Field(
        default=DocumentType.MANUFACTURER_CARD,
        description="Always kb_manufacturer_card",
    )

    # Manufacturer-specific summary fields
    company_name: str = Field(
        ...,
        description="Company name",
    )
    headquarters: Optional[str] = Field(
        None,
        description="Headquarters location",
    )
    founded: Optional[str] = Field(
        None,
        description="Year founded",
    )

    @classmethod
    def from_document(
        cls, doc: ManufacturerCardDocument
    ) -> "ManufacturerCardSummary":
        """Create summary from full manufacturer card."""
        return cls(
            _id=doc.id or "",
            document_type=doc.metadata_content.document_type,
            content_type=doc.metadata_content.content_type,
            title=doc.metadata_content.title,
            clinical_domain=doc.metadata_content.clinical_domain,
            tags=doc.metadata_content.tags,
            created_at=doc.metadata_object.created_at,
            updated_at=doc.metadata_object.updated_at,
            company_name=doc.metadata_content.company_name,
            headquarters=doc.metadata_content.headquarters,
            founded=doc.metadata_content.founded,
        )
