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
Evidence document schemas for kb_evidence_docs collection.

Peer-reviewed papers, clinical trials, and other evidence documents
with structured sections, figures, tables, and references.

Reference: docs/Plans/DocumentDataModelSchema-Normalize-2025-11-15/
"""

from datetime import date
from typing import Optional

from pydantic import Field

from ashmatics_datamodels.documents.base import (
    CitationReference,
    ContentBase,
    ContentType,
    DocumentSummaryBase,
    DocumentType,
    FigureReference,
    MetadataContentBase,
    MetadataObjectBase,
    MongoDocumentBase,
    SectionBase,
    TableReference,
)


# =============================================================================
# Evidence-Specific Metadata Content
# =============================================================================


class EvidenceMetadataContent(MetadataContentBase):
    """
    Metadata content specific to evidence documents (publications).

    Extends base metadata with publication-specific fields like
    authors, journal, DOI, and anatomical focus.
    """

    document_type: DocumentType = Field(
        default=DocumentType.EVIDENCE_DOC,
        description="Always 'kb_evidence_doc' for evidence documents",
    )
    content_type: ContentType = Field(
        default=ContentType.PEER_REVIEWED_PAPER,
        description="Type of evidence (peer_reviewed_paper, preprint, etc.)",
    )

    # Publication metadata
    publication_date: Optional[date] = Field(
        None,
        description="Date of publication",
    )
    authors: list[str] = Field(
        default_factory=list,
        description="List of author names",
    )
    journal: Optional[str] = Field(
        None,
        description="Journal or venue name",
    )
    doi: Optional[str] = Field(
        None,
        description="Digital Object Identifier",
    )
    pubmed_id: Optional[str] = Field(
        None,
        description="PubMed ID (PMID)",
    )

    # Clinical focus
    anatomical_region: Optional[str] = Field(
        None,
        description="Primary anatomical region (e.g., 'chest', 'brain')",
    )
    pathology_focus: list[str] = Field(
        default_factory=list,
        description="Pathologies studied (e.g., ['pneumonia', 'pleural_effusion'])",
    )


# =============================================================================
# Evidence-Specific Content
# =============================================================================


class EvidenceContent(ContentBase):
    """
    Content structure for evidence documents.

    Standard academic paper structure with introduction, methods,
    results, discussion, and conclusion sections.
    """

    sections: dict[str, SectionBase] = Field(
        default_factory=lambda: {
            "1_introduction": SectionBase(title="Introduction", order=1),
            "2_methods": SectionBase(title="Methods", order=2),
            "3_results": SectionBase(title="Results", order=3),
            "4_discussion": SectionBase(title="Discussion", order=4),
            "5_conclusion": SectionBase(title="Conclusion", order=5),
        },
        description="Standard academic paper sections",
    )
    figures: list[FigureReference] = Field(
        default_factory=list,
        description="Figures in the paper",
    )
    tables: list[TableReference] = Field(
        default_factory=list,
        description="Tables in the paper",
    )
    references: list[CitationReference] = Field(
        default_factory=list,
        description="Bibliography",
    )


# =============================================================================
# Complete Evidence Document
# =============================================================================


class EvidenceDocument(MongoDocumentBase):
    """
    Complete evidence document with three-tier structure.

    Used for kb_evidence_docs MongoDB collection.
    """

    metadata_object: MetadataObjectBase = Field(
        default_factory=MetadataObjectBase,
        description="Artifact metadata",
    )
    metadata_content: EvidenceMetadataContent = Field(
        ...,
        description="Evidence-specific metadata",
    )
    content: EvidenceContent = Field(
        default_factory=EvidenceContent,
        description="Paper content with sections",
    )


class EvidenceDocumentCreate(MongoDocumentBase):
    """Schema for creating a new evidence document."""

    metadata_content: EvidenceMetadataContent = Field(
        ...,
        description="Required evidence metadata",
    )
    content: EvidenceContent = Field(
        default_factory=EvidenceContent,
        description="Paper content",
    )


# =============================================================================
# Evidence Summary
# =============================================================================


class EvidenceSummary(DocumentSummaryBase):
    """
    Summary view for evidence documents in listings.

    Flattens key publication metadata for search results.
    """

    document_type: DocumentType = Field(
        default=DocumentType.EVIDENCE_DOC,
        description="Always kb_evidence_doc",
    )

    # Publication-specific summary fields
    authors: list[str] = Field(
        default_factory=list,
        description="Author list",
    )
    journal: Optional[str] = Field(
        None,
        description="Journal name",
    )
    publication_date: Optional[date] = Field(
        None,
        description="Publication date",
    )
    doi: Optional[str] = Field(
        None,
        description="DOI",
    )
    abstract: Optional[str] = Field(
        None,
        description="Paper abstract",
    )
    anatomical_region: Optional[str] = Field(
        None,
        description="Anatomical focus",
    )

    @classmethod
    def from_document(cls, doc: EvidenceDocument) -> "EvidenceSummary":
        """Create summary from full evidence document."""
        return cls(
            _id=doc.id or "",
            document_type=doc.metadata_content.document_type,
            content_type=doc.metadata_content.content_type,
            title=doc.metadata_content.title,
            clinical_domain=doc.metadata_content.clinical_domain,
            tags=doc.metadata_content.tags,
            created_at=doc.metadata_object.created_at,
            updated_at=doc.metadata_object.updated_at,
            authors=doc.metadata_content.authors,
            journal=doc.metadata_content.journal,
            publication_date=doc.metadata_content.publication_date,
            doi=doc.metadata_content.doi,
            abstract=doc.metadata_content.abstract,
            anatomical_region=doc.metadata_content.anatomical_region,
        )
