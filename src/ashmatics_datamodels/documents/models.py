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
AI Model Card schemas for kb_aimodel_cards collection.

Structured model cards with architecture, training data,
performance metrics, limitations, and intended use sections.

Reference: docs/Plans/DocumentDataModelSchema-Normalize-2025-11-15/
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
# Model Card Nested Schemas
# =============================================================================


class InputSpecs(AshMaticsBaseModel):
    """Model input specifications."""

    image_size: Optional[list[int]] = Field(
        None,
        description="Input image dimensions [height, width]",
    )
    channels: Optional[int] = Field(
        None,
        description="Number of input channels",
    )
    format: Optional[str] = Field(
        None,
        description="Input format (e.g., 'DICOM', 'PNG')",
    )
    additional_inputs: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional input specifications",
    )


class OutputSpecs(AshMaticsBaseModel):
    """Model output specifications."""

    classes: list[str] = Field(
        default_factory=list,
        description="Output class labels",
    )
    output_format: Optional[str] = Field(
        None,
        description="Output format (e.g., 'probability_distribution', 'bounding_boxes')",
    )
    additional_outputs: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional output specifications",
    )


class DataSplits(AshMaticsBaseModel):
    """Training data split ratios."""

    train: float = Field(
        0.7,
        ge=0.0,
        le=1.0,
        description="Training set ratio",
    )
    val: float = Field(
        0.15,
        ge=0.0,
        le=1.0,
        description="Validation set ratio",
    )
    test: float = Field(
        0.15,
        ge=0.0,
        le=1.0,
        description="Test set ratio",
    )


class PerformanceMetrics(AshMaticsBaseModel):
    """Model performance metrics."""

    accuracy: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Overall accuracy",
    )
    sensitivity: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Sensitivity (recall)",
    )
    specificity: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Specificity",
    )
    auc_roc: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Area under ROC curve",
    )
    f1_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="F1 score",
    )
    validation_dataset: Optional[str] = Field(
        None,
        description="Dataset used for validation",
    )
    additional_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metrics",
    )


class ExternalResources(AshMaticsBaseModel):
    """Links to external resources."""

    github: Optional[str] = Field(
        None,
        description="GitHub repository URL",
    )
    huggingface: Optional[str] = Field(
        None,
        description="Hugging Face model URL",
    )
    paper_doi: Optional[str] = Field(
        None,
        description="DOI of associated paper",
    )
    documentation: Optional[str] = Field(
        None,
        description="Documentation URL",
    )


# =============================================================================
# Model Card Sections
# =============================================================================


class ModelOverviewSection(SectionBase):
    """Model overview section with architecture details."""

    title: str = Field(default="Model Overview", description="Section title")
    order: int = Field(default=1, description="Section order")
    architecture: Optional[str] = Field(
        None,
        description="Model architecture (e.g., 'ResNet-50', 'ViT-B/16')",
    )
    framework: Optional[str] = Field(
        None,
        description="ML framework (e.g., 'PyTorch 2.0', 'TensorFlow 2.x')",
    )
    input_specs: Optional[InputSpecs] = Field(
        None,
        description="Input specifications",
    )
    output_specs: Optional[OutputSpecs] = Field(
        None,
        description="Output specifications",
    )


class TrainingDataSection(SectionBase):
    """Training data section."""

    title: str = Field(default="Training Data", description="Section title")
    order: int = Field(default=2, description="Section order")
    dataset_name: Optional[str] = Field(
        None,
        description="Name of training dataset",
    )
    dataset_size: Optional[int] = Field(
        None,
        ge=0,
        description="Number of samples in dataset",
    )
    data_splits: Optional[DataSplits] = Field(
        None,
        description="Train/val/test split ratios",
    )
    data_source: Optional[str] = Field(
        None,
        description="Source of training data",
    )
    inclusion_criteria: Optional[str] = Field(
        None,
        description="Data inclusion criteria",
    )
    exclusion_criteria: Optional[str] = Field(
        None,
        description="Data exclusion criteria",
    )


class PerformanceSection(SectionBase):
    """Performance metrics section."""

    title: str = Field(default="Performance", description="Section title")
    order: int = Field(default=3, description="Section order")
    metrics: Optional[PerformanceMetrics] = Field(
        None,
        description="Performance metrics",
    )


class LimitationsSection(SectionBase):
    """Limitations and biases section."""

    title: str = Field(default="Limitations & Biases", description="Section title")
    order: int = Field(default=4, description="Section order")
    known_limitations: list[str] = Field(
        default_factory=list,
        description="Known limitations",
    )
    bias_considerations: list[str] = Field(
        default_factory=list,
        description="Potential biases",
    )


class IntendedUseSection(SectionBase):
    """Intended use section."""

    title: str = Field(default="Intended Use", description="Section title")
    order: int = Field(default=5, description="Section order")
    clinical_applications: list[str] = Field(
        default_factory=list,
        description="Intended clinical applications",
    )
    contraindications: list[str] = Field(
        default_factory=list,
        description="Contraindications and warnings",
    )


# =============================================================================
# Model Card Metadata Content
# =============================================================================


class ModelCardMetadataContent(MetadataContentBase):
    """
    Metadata content specific to AI model cards.
    """

    document_type: DocumentType = Field(
        default=DocumentType.AIMODEL_CARD,
        description="Always 'kb_aimodel_card'",
    )
    content_type: ContentType = Field(
        default=ContentType.MODEL_CARD_V1,
        description="Model card format version",
    )

    # Model identification
    model_name: str = Field(
        ...,
        description="Model name",
    )
    model_version: Optional[str] = Field(
        None,
        description="Model version string",
    )
    developer: Optional[str] = Field(
        None,
        description="Model developer/organization",
    )
    last_updated: Optional[date] = Field(
        None,
        description="Date of last model update",
    )

    # Clinical focus
    anatomical_region: Optional[str] = Field(
        None,
        description="Primary anatomical region",
    )


# =============================================================================
# Model Card Content
# =============================================================================


class ModelCardContent(ContentBase):
    """
    Content structure for AI model cards.
    """

    sections: dict[str, SectionBase] = Field(
        default_factory=lambda: {
            "model_overview": ModelOverviewSection(title="Model Overview", order=1),
            "training_data": TrainingDataSection(title="Training Data", order=2),
            "performance_metrics": PerformanceSection(title="Performance", order=3),
            "limitations": LimitationsSection(title="Limitations & Biases", order=4),
            "intended_use": IntendedUseSection(title="Intended Use", order=5),
        },
        description="Model card sections",
    )
    external_resources: Optional[ExternalResources] = Field(
        None,
        description="Links to external resources",
    )


# =============================================================================
# Complete Model Card Document
# =============================================================================


class ModelCardDocument(MongoDocumentBase):
    """
    Complete AI model card with three-tier structure.

    Used for kb_aimodel_cards MongoDB collection.
    """

    metadata_object: MetadataObjectBase = Field(
        default_factory=MetadataObjectBase,
        description="Artifact metadata",
    )
    metadata_content: ModelCardMetadataContent = Field(
        ...,
        description="Model card metadata",
    )
    content: ModelCardContent = Field(
        default_factory=ModelCardContent,
        description="Model card content",
    )


class ModelCardDocumentCreate(MongoDocumentBase):
    """Schema for creating a new model card."""

    metadata_content: ModelCardMetadataContent = Field(
        ...,
        description="Required model card metadata",
    )
    content: ModelCardContent = Field(
        default_factory=ModelCardContent,
        description="Model card content",
    )


# =============================================================================
# Model Card Summary
# =============================================================================


class ModelCardSummary(DocumentSummaryBase):
    """
    Summary view for model cards in listings.
    """

    document_type: DocumentType = Field(
        default=DocumentType.AIMODEL_CARD,
        description="Always kb_aimodel_card",
    )

    # Model-specific summary fields
    model_name: str = Field(
        ...,
        description="Model name",
    )
    model_version: Optional[str] = Field(
        None,
        description="Model version",
    )
    developer: Optional[str] = Field(
        None,
        description="Developer/organization",
    )
    anatomical_region: Optional[str] = Field(
        None,
        description="Anatomical focus",
    )

    @classmethod
    def from_document(cls, doc: ModelCardDocument) -> "ModelCardSummary":
        """Create summary from full model card."""
        return cls(
            _id=doc.id or "",
            document_type=doc.metadata_content.document_type,
            content_type=doc.metadata_content.content_type,
            title=doc.metadata_content.title,
            clinical_domain=doc.metadata_content.clinical_domain,
            tags=doc.metadata_content.tags,
            created_at=doc.metadata_object.created_at,
            updated_at=doc.metadata_object.updated_at,
            model_name=doc.metadata_content.model_name,
            model_version=doc.metadata_content.model_version,
            developer=doc.metadata_content.developer,
            anatomical_region=doc.metadata_content.anatomical_region,
        )
