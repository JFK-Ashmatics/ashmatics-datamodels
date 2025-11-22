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
Regulatory document schemas for kb_regulatory_docs collection.

FDA 510(k) summaries, PMA summaries, and De Novo summaries
with structured sections for device description, indications,
predicates, and performance testing.

Reference: docs/Plans/DocumentDataModelSchema-Normalize-2025-11-15/
Vocabulary: https://open.fda.gov/device/510k/
"""

from datetime import date
from typing import Any, Optional

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
# Regulatory-Specific Nested Schemas
# =============================================================================


class RawSection(SectionBase):
    """
    Raw parsed section from document parser (e.g., Docling).

    Stores all sections parsed from the original document,
    not just the enriched/normalized sections. Enables full
    document reconstruction and verification.
    """

    section_id: str = Field(
        ...,
        description="Unique identifier for this raw section (e.g., 'section_1')",
    )
    normalized_to: Optional[str] = Field(
        None,
        description="Key of enriched section this maps to (e.g., '2_indications_for_use'). None if not normalized.",
    )


class StructuredIndication(AshMaticsBaseModel):
    """Structured representation of indications for use."""

    anatomical_region: Optional[str] = Field(
        None,
        description="Target anatomical region",
    )
    modality: Optional[str] = Field(
        None,
        description="Imaging or diagnostic modality",
    )
    clinical_application: Optional[str] = Field(
        None,
        description="Primary clinical application",
    )
    patient_population: Optional[str] = Field(
        None,
        description="Target patient population",
    )


class PredicateDeviceInfo(AshMaticsBaseModel):
    """Information about a predicate device for substantial equivalence."""

    k_number: str = Field(
        ...,
        description="510(k) number of predicate device",
    )
    device_name: Optional[str] = Field(
        None,
        description="Name of the predicate device",
    )
    manufacturer: Optional[str] = Field(
        None,
        description="Manufacturer of predicate device",
    )
    comparison_summary: Optional[str] = Field(
        None,
        description="Summary of comparison to predicate",
    )


class PerformanceTestResults(AshMaticsBaseModel):
    """Structured performance testing results."""

    sensitivity: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Sensitivity (true positive rate)",
    )
    specificity: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Specificity (true negative rate)",
    )
    auc_roc: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Area under ROC curve",
    )
    test_dataset_size: Optional[int] = Field(
        None,
        ge=0,
        description="Number of cases in test dataset",
    )
    comparison_to_predicate: Optional[str] = Field(
        None,
        description="Comparison result (e.g., 'Non-inferior')",
    )
    additional_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional performance metrics",
    )


# =============================================================================
# Regulatory-Specific Sections
# =============================================================================


class SponsorSection(SectionBase):
    """
    Sponsor/Applicant identification section.

    Contains sponsor company information, contact details,
    and submission metadata commonly found at the beginning
    of 510(k) and De Novo summary documents.
    """

    title: str = Field(default="Sponsor Information", description="Section title")
    order: int = Field(default=0, description="Section order")


class DeviceDescriptionSection(SectionBase):
    """Device description section with structured fields."""

    title: str = Field(default="Device Description", description="Section title")
    order: int = Field(default=1, description="Section order")


class IndicationsSection(SectionBase):
    """Indications for use section with structured data."""

    title: str = Field(default="Indications for Use", description="Section title")
    order: int = Field(default=2, description="Section order")
    structured_indications: Optional[StructuredIndication] = Field(
        None,
        description="Structured indication data",
    )


class PredicatesSection(SectionBase):
    """Predicate devices section."""

    title: str = Field(default="Predicate Devices", description="Section title")
    order: int = Field(default=3, description="Section order")
    predicates: list[PredicateDeviceInfo] = Field(
        default_factory=list,
        description="List of predicate devices",
    )


class PerformanceTestingSection(SectionBase):
    """Performance testing section with results."""

    title: str = Field(default="Performance Testing", description="Section title")
    order: int = Field(default=4, description="Section order")
    test_results: Optional[PerformanceTestResults] = Field(
        None,
        description="Structured test results",
    )


class SubstantialEquivalenceSection(SectionBase):
    """Substantial equivalence determination section."""

    title: str = Field(default="Substantial Equivalence", description="Section title")
    order: int = Field(default=5, description="Section order")


# =============================================================================
# Regulatory-Specific Metadata Content
# =============================================================================


class RegulatoryMetadataContent(MetadataContentBase):
    """
    Metadata content specific to regulatory documents.

    Extends base metadata with FDA-specific fields aligned
    with OpenFDA vocabulary.
    """

    document_type: DocumentType = Field(
        default=DocumentType.REGULATORY_DOC,
        description="Always 'kb_regulatory_doc' for regulatory documents",
    )
    content_type: ContentType = Field(
        default=ContentType.SUMMARY_510K,
        description="Type of regulatory document",
    )

    # FDA identifiers (OpenFDA aligned)
    k_number: Optional[str] = Field(
        None,
        max_length=10,
        description="510(k) number (e.g., 'K240001')",
    )
    pma_number: Optional[str] = Field(
        None,
        max_length=10,
        description="PMA number (e.g., 'P190001')",
    )
    de_novo_number: Optional[str] = Field(
        None,
        max_length=15,
        description="De Novo number",
    )

    # Device and applicant info
    clearance_date: Optional[date] = Field(
        None,
        description="Date of FDA clearance/approval",
    )
    applicant: Optional[str] = Field(
        None,
        description="Applicant/submitter name",
    )
    device_name: Optional[str] = Field(
        None,
        description="Device name as cleared",
    )
    device_class: Optional[str] = Field(
        None,
        max_length=3,
        description="FDA device class (I, II, III)",
    )
    product_code: Optional[str] = Field(
        None,
        description="FDA three-letter product code(s). Single code (e.g., 'QIH') or comma-separated for multiple (e.g., 'QIH,LLZ')",
    )

    # Advisory committee
    advisory_committee: Optional[str] = Field(
        None,
        max_length=2,
        description="Two-letter advisory committee code",
    )


# =============================================================================
# Regulatory-Specific Content
# =============================================================================


class RegulatoryContent(ContentBase):
    """
    Content structure for regulatory documents.

    Standard 510(k) summary structure with device description,
    indications, predicates, testing, and substantial equivalence.

    Includes both enriched/normalized sections and raw parsed sections
    for complete document preservation and traceability.
    """

    sections: dict[str, SectionBase] = Field(
        default_factory=lambda: {
            "0_sponsor": SponsorSection(
                title="Sponsor Information", order=0
            ),
            "1_device_description": DeviceDescriptionSection(
                title="Device Description", order=1
            ),
            "2_indications_for_use": IndicationsSection(
                title="Indications for Use", order=2
            ),
            "3_predicate_devices": PredicatesSection(
                title="Predicate Devices", order=3
            ),
            "4_performance_testing": PerformanceTestingSection(
                title="Performance Testing", order=4
            ),
            "5_substantial_equivalence": SubstantialEquivalenceSection(
                title="Substantial Equivalence", order=5
            ),
        },
        description="Enriched/normalized 510(k) summary sections (Ashmatics value-add)",
    )

    raw_sections: list[RawSection] = Field(
        default_factory=list,
        description="All sections parsed from document (complete content from parser like Docling)",
    )


# =============================================================================
# Complete Regulatory Document
# =============================================================================


class RegulatoryDocument(MongoDocumentBase):
    """
    Complete regulatory document with three-tier structure.

    Used for kb_regulatory_docs MongoDB collection.
    """

    metadata_object: MetadataObjectBase = Field(
        default_factory=MetadataObjectBase,
        description="Artifact metadata",
    )
    metadata_content: RegulatoryMetadataContent = Field(
        ...,
        description="Regulatory-specific metadata",
    )
    content: RegulatoryContent = Field(
        default_factory=RegulatoryContent,
        description="510(k) summary content",
    )


class RegulatoryDocumentCreate(MongoDocumentBase):
    """Schema for creating a new regulatory document."""

    metadata_content: RegulatoryMetadataContent = Field(
        ...,
        description="Required regulatory metadata",
    )
    content: RegulatoryContent = Field(
        default_factory=RegulatoryContent,
        description="Document content",
    )


# =============================================================================
# Regulatory Summary
# =============================================================================


class RegulatorySummary(DocumentSummaryBase):
    """
    Summary view for regulatory documents in listings.

    Flattens key FDA metadata for search results.
    """

    document_type: DocumentType = Field(
        default=DocumentType.REGULATORY_DOC,
        description="Always kb_regulatory_doc",
    )

    # FDA-specific summary fields
    k_number: Optional[str] = Field(
        None,
        description="510(k) number",
    )
    pma_number: Optional[str] = Field(
        None,
        description="PMA number",
    )
    clearance_date: Optional[date] = Field(
        None,
        description="Clearance/approval date",
    )
    applicant: Optional[str] = Field(
        None,
        description="Applicant name",
    )
    device_name: Optional[str] = Field(
        None,
        description="Device name",
    )
    device_class: Optional[str] = Field(
        None,
        description="Device class",
    )
    product_code: Optional[str] = Field(
        None,
        description="Product code",
    )

    @classmethod
    def from_document(cls, doc: RegulatoryDocument) -> "RegulatorySummary":
        """Create summary from full regulatory document."""
        return cls(
            _id=doc.id or "",
            document_type=doc.metadata_content.document_type,
            content_type=doc.metadata_content.content_type,
            title=doc.metadata_content.title,
            clinical_domain=doc.metadata_content.clinical_domain,
            tags=doc.metadata_content.tags,
            created_at=doc.metadata_object.created_at,
            updated_at=doc.metadata_object.updated_at,
            k_number=doc.metadata_content.k_number,
            pma_number=doc.metadata_content.pma_number,
            clearance_date=doc.metadata_content.clearance_date,
            applicant=doc.metadata_content.applicant,
            device_name=doc.metadata_content.device_name,
            device_class=doc.metadata_content.device_class,
            product_code=doc.metadata_content.product_code,
        )
