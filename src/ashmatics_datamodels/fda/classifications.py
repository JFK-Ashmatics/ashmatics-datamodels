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
FDA device classification and product code schemas.

Includes:
- FDA_ProductCode: Three-letter product code definitions
- FDA_DeviceClassification: OpenFDA classification records
- ProductClassificationSystem: Multi-jurisdiction classification systems (CDRH, EMDN, GMDN, ARTG)
- ProductClassification: Individual classification codes within systems

Reference: 21 CFR Parts 862-892 (Device Classification Regulations)
Vocabulary Source: OpenFDA Device Classification API

Migrated from: KB src/app/schemas/product_classification_schema.py
               KB src/app/schemas/product_classification_system_schema.py
"""

from datetime import datetime
from typing import Optional

from pydantic import AliasChoices, Field, computed_field, field_validator

from ashmatics_datamodels.common.base import AshMaticsBaseModel, TimestampedModel
from ashmatics_datamodels.common.enums import RiskCategory
from ashmatics_datamodels.common.validators import validate_product_code
from ashmatics_datamodels.fda.enums import FDA_DeviceClass, ReviewPanel, SubmissionType


class FDA_ProductCode(AshMaticsBaseModel):
    """
    FDA Product Code definition.

    Product codes are three-letter codes assigned by FDA to categorize
    medical devices based on their intended use. Each product code maps
    to a specific device classification regulation.

    Vocabulary Source: https://open.fda.gov/device/classification/
    """

    product_code: str = Field(
        ...,
        max_length=3,
        min_length=3,
        description="Three-letter FDA product code (e.g., 'MYN', 'LLZ')",
    )
    device_name: str = Field(
        ..., max_length=500, description="Official FDA device name for this product code"
    )
    device_class: FDA_DeviceClass = Field(
        ..., description="FDA device classification (1, 2, or 3)"
    )

    # Regulatory details
    regulation_number: Optional[str] = Field(
        None,
        max_length=20,
        description="21 CFR regulation number (e.g., '892.2050')",
    )
    submission_type: Optional[SubmissionType] = Field(
        None, description="Typical submission pathway for this product code"
    )
    review_panel: Optional[ReviewPanel] = Field(
        None, description="FDA review panel responsible for this device type"
    )

    # Exemption status
    gmp_exempt: Optional[bool] = Field(
        None, description="Whether device is exempt from GMP (21 CFR Part 820)"
    )
    premarket_exempt: Optional[bool] = Field(
        None, description="Whether device is exempt from premarket notification"
    )

    # Definition and scope
    definition: Optional[str] = Field(
        None, description="FDA regulatory definition of this device type"
    )

    @field_validator("product_code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        result = validate_product_code(v)
        if result is None:
            raise ValueError("product_code is required")
        return result

    @computed_field
    @property
    def cfr_reference(self) -> Optional[str]:
        """Get full CFR reference if regulation number is available."""
        if self.regulation_number:
            return f"21 CFR {self.regulation_number}"
        return None


class FDA_DeviceClassification(AshMaticsBaseModel):
    """
    Complete FDA device classification record.

    Represents a specific device classification including product code,
    device class, regulatory requirements, and special controls.

    This schema aligns with OpenFDA Device Classification API responses.
    """

    # Identifiers
    product_code: str = Field(..., max_length=3, description="Three-letter product code")
    device_name: str = Field(..., max_length=500, description="FDA device name")
    device_class: FDA_DeviceClass = Field(..., description="Device classification")

    # Regulatory pathway
    regulation_number: Optional[str] = Field(
        None, description="21 CFR regulation number"
    )
    submission_type_id: Optional[SubmissionType] = Field(
        None, description="Required submission type"
    )
    review_panel: Optional[ReviewPanel] = Field(None, description="Review panel code")

    # Medical specialty
    medical_specialty: Optional[str] = Field(
        None, max_length=100, description="Medical specialty category"
    )
    medical_specialty_description: Optional[str] = Field(
        None, description="Full description of medical specialty"
    )

    # Exemptions and requirements
    gmp_exempt_flag: Optional[str] = Field(
        None, description="GMP exemption flag (Y/N)"
    )
    premarket_exempt: Optional[str] = Field(
        None, description="Premarket exemption status"
    )
    summary_malfunction_reporting: Optional[str] = Field(
        None, description="Summary malfunction reporting eligibility"
    )

    # Life-sustaining/supporting
    life_sustain_support_flag: Optional[str] = Field(
        None, description="Whether device is life-sustaining or life-supporting"
    )
    implant_flag: Optional[str] = Field(
        None, description="Whether device is an implant"
    )

    # Definition
    definition: Optional[str] = Field(
        None, description="Regulatory definition of device type"
    )

    @field_validator("product_code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        result = validate_product_code(v)
        if result is None:
            raise ValueError("product_code is required")
        return result

    @computed_field
    @property
    def is_class_3(self) -> bool:
        """Check if this is a Class III (high-risk) device."""
        return self.device_class == FDA_DeviceClass.CLASS_3

    @computed_field
    @property
    def requires_pma(self) -> bool:
        """Check if device typically requires PMA."""
        return (
            self.device_class == FDA_DeviceClass.CLASS_3
            and self.submission_type_id == SubmissionType.PMA
        )

    @computed_field
    @property
    def is_life_sustaining(self) -> bool:
        """Check if device is life-sustaining or life-supporting."""
        if self.life_sustain_support_flag:
            return self.life_sustain_support_flag.upper() == "Y"
        return False


# =============================================================================
# Product Classification System (Multi-Jurisdiction)
# =============================================================================


class ProductClassificationSystemBase(AshMaticsBaseModel):
    """
    Base schema for product classification systems.

    Classification systems are jurisdiction-specific taxonomies for
    categorizing medical devices (CDRH, EMDN, GMDN, ARTG, etc.).
    """

    system_code: str = Field(
        ...,
        max_length=50,
        description="Unique system code (CDRH, EMDN, GMDN, ARTG)",
    )
    system_name: str = Field(
        ...,
        max_length=255,
        description="Full system name",
    )
    version: Optional[str] = Field(
        None,
        max_length=50,
        description="System version",
    )
    description: Optional[str] = Field(
        None,
        description="Detailed system description",
    )
    official_url: Optional[str] = Field(
        None,
        max_length=500,
        description="Official website or documentation URL",
    )
    is_active: bool = Field(
        True,
        description="Whether system is currently active",
    )


class ProductClassificationSystemCreate(ProductClassificationSystemBase):
    """Schema for creating a new product classification system."""

    regulator_id: Optional[int] = Field(
        None,
        gt=0,
        description="Foreign key to regulators (nullable for global systems like GMDN)",
    )


class ProductClassificationSystemResponse(ProductClassificationSystemBase, TimestampedModel):
    """Schema for product classification system responses."""

    id: Optional[int] = Field(None, description="Classification system ID")
    regulator_id: Optional[int] = Field(None, description="Foreign key to regulator")

    # Computed fields
    classification_count: int = Field(
        0, description="Number of classifications in this system"
    )


class ClassificationSystemInfo(AshMaticsBaseModel):
    """Nested schema for classification system information."""

    id: int
    system_code: str
    system_name: str
    version: Optional[str] = None
    regulator_code: Optional[str] = None


# =============================================================================
# Product Classification (Individual Codes within Systems)
# =============================================================================


class ProductClassificationBase(AshMaticsBaseModel):
    """
    Base schema for product classifications.

    Individual classification codes within a classification system
    (e.g., LLZ within CDRH, 12345 within GMDN).
    """

    code: str = Field(
        ...,
        max_length=50,
        validation_alias=AliasChoices("code", "product_code"),
        description="Classification code (FDA: product_code)",
    )
    description: str = Field(
        ...,
        max_length=500,
        description="Short description of the classification",
    )
    device_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Common device name",
    )
    device_class: Optional[str] = Field(
        None,
        max_length=10,
        description="Device class: 1, 2, 3 (FDA) or I, IIa, IIb, III (EU MDR)",
    )
    risk_category: Optional[RiskCategory] = Field(
        None,
        description="Risk category (low, moderate, high)",
    )
    definition: Optional[str] = Field(
        None,
        description="Detailed classification definition",
    )
    regulation_number: Optional[str] = Field(
        None,
        max_length=50,
        description="Regulatory reference (e.g., 21 CFR 880.6310)",
    )
    medical_specialty: Optional[str] = Field(
        None,
        max_length=255,
        validation_alias=AliasChoices("medical_specialty", "medical_specialty_description"),
        description="Associated medical specialty (FDA: medical_specialty_description)",
    )
    review_panel: Optional[str] = Field(
        None,
        max_length=255,
        description="Regulatory review panel",
    )
    target_area: Optional[str] = Field(
        None,
        max_length=255,
        description="Target anatomical area or application",
    )
    technical_method: Optional[str] = Field(
        None,
        description="Technical method or approach",
    )
    is_active: bool = Field(True, description="Whether classification is currently active")

    # FDA-specific flags
    gmp_exempt_flag: Optional[bool] = Field(
        None,
        description="FDA: Whether device is exempt from GMP (21 CFR 820)",
    )
    implant_flag: Optional[bool] = Field(
        None,
        description="FDA: Whether device is implantable",
    )
    life_sustain_support_flag: Optional[bool] = Field(
        None,
        description="FDA: Whether device is life-sustaining or life-supporting",
    )
    submission_type: Optional[SubmissionType] = Field(
        None,
        description="FDA: Required submission pathway (510(k), PMA, De Novo, Exempt)",
    )


class ProductClassificationCreate(ProductClassificationBase):
    """Schema for creating a new product classification."""

    classification_system_id: int = Field(
        ...,
        gt=0,
        description="Foreign key to product_classification_systems",
    )


class ProductClassificationResponse(ProductClassificationBase, TimestampedModel):
    """Schema for product classification responses."""

    id: Optional[int] = Field(None, description="Primary key")
    classification_system_id: int = Field(
        ..., description="Foreign key to classification system"
    )

    # Nested classification system info
    classification_system: Optional[ClassificationSystemInfo] = Field(
        None, description="Nested classification system information"
    )

    @computed_field
    @property
    def full_code(self) -> str:
        """Full code with system prefix (e.g., 'CDRH:LLZ')."""
        if self.classification_system:
            return f"{self.classification_system.system_code}:{self.code}"
        return self.code
