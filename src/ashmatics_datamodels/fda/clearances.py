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
FDA clearance and approval schemas.

Includes:
- FDA_510kClearance: 510(k) premarket notifications
- FDA_PMAClearance: Premarket Approval applications
- FDA_DeNovoClearance: De Novo classification requests
- RegulatoryAuthorization: Generic authorization lifecycle tracking

Covers 510(k), PMA, De Novo, and other FDA premarket pathways.

Reference: 21 CFR Parts 807, 814, 860
Vocabulary Source: OpenFDA Device 510k API (https://open.fda.gov/device/510k/)

Migrated from: KB src/app/schemas/regulatory_authorization_schema.py
JIRA: ASHKBAPP-28 (Phase 2.3)
"""

from datetime import date
from typing import Optional

from pydantic import AliasChoices, Field, computed_field, field_validator

from ashmatics_datamodels.common.base import AshMaticsBaseModel, AuditedModel, TimestampedModel
from ashmatics_datamodels.common.enums import AuthorizationStatus
from ashmatics_datamodels.common.validators import (
    validate_iso_date,
    validate_k_number_format,
    validate_pma_number_format,
    validate_product_code,
)
from ashmatics_datamodels.fda.enums import (
    ClearanceType,
    FDA_DeviceClass,
    ReviewPanel,
    SubmissionType,
)


class FDA_PredicateDevice(AshMaticsBaseModel):
    """
    Predicate device referenced in 510(k) substantial equivalence.

    A predicate device is a legally marketed device to which a new device
    is compared to demonstrate substantial equivalence.
    """

    k_number: Optional[str] = Field(
        None, description="510(k) number of predicate device"
    )
    pma_number: Optional[str] = Field(
        None, description="PMA number if predicate is PMA-approved"
    )
    device_name: Optional[str] = Field(
        None, max_length=500, description="Name of predicate device"
    )
    manufacturer: Optional[str] = Field(
        None, max_length=255, description="Manufacturer of predicate device"
    )
    comparison_summary: Optional[str] = Field(
        None, description="Summary of substantial equivalence comparison"
    )

    @field_validator("k_number")
    @classmethod
    def validate_k(cls, v: Optional[str]) -> Optional[str]:
        return validate_k_number_format(v)


class FDA_ClearanceBase(AshMaticsBaseModel):
    """
    Base schema for FDA clearances/approvals.

    Common fields across all FDA premarket pathways.
    """

    # Device identification
    device_name: str = Field(
        ..., max_length=500, description="FDA-registered device name"
    )
    device_class: Optional[FDA_DeviceClass] = Field(
        None, description="FDA device classification (1, 2, or 3)"
    )
    product_code: Optional[str] = Field(
        None,
        max_length=3,
        description="Three-letter FDA product code",
    )
    regulation_number: Optional[str] = Field(
        None,
        max_length=20,
        description="21 CFR regulation number (e.g., '892.2050')",
    )

    # Submission details
    submission_type: Optional[SubmissionType] = Field(
        None, description="Type of premarket submission"
    )
    review_panel: Optional[ReviewPanel] = Field(
        None, description="FDA review panel code"
    )

    # Parties
    applicant: Optional[str] = Field(
        None, max_length=255, description="Entity submitting the application"
    )
    manufacturer_name: Optional[str] = Field(
        None, max_length=255, description="Device manufacturer"
    )

    # Indications
    indications_for_use: Optional[str] = Field(
        None, description="Cleared/approved indications for use statement"
    )
    intended_use_summary: Optional[str] = Field(
        None, description="Brief summary of intended use"
    )

    @field_validator("product_code")
    @classmethod
    def validate_product_code_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_product_code(v)


class FDA_510kClearance(FDA_ClearanceBase):
    """
    FDA 510(k) Premarket Notification clearance.

    The 510(k) is a premarket submission demonstrating that the device
    is substantially equivalent to a legally marketed predicate device.

    Reference: 21 CFR Part 807 Subpart E
    Vocabulary Source: https://open.fda.gov/device/510k/
    """

    # 510(k) specific identifiers
    k_number: str = Field(
        ...,
        description=(
            "FDA-assigned premarket notification number. "
            "Leading letters: 'K' = 510(k), 'BK' = 510(k) by CBER, 'DEN' = De Novo"
        ),
        examples=["K240001", "DEN180067", "BK200001"],
    )

    # Dates (using OpenFDA field names)
    date_received: Optional[date] = Field(
        None, description="Date FDA received the 510(k) submission"
    )
    decision_date: Optional[date] = Field(
        None,
        description="Date of FDA decision (clearance or not substantially equivalent)",
    )

    # Decision
    decision_code: Optional[str] = Field(
        None,
        max_length=10,
        description="FDA decision code (e.g., 'SESE' for substantially equivalent)",
    )
    decision_description: Optional[str] = Field(
        None, description="Full description of FDA decision"
    )

    # Predicate devices
    predicate_devices: Optional[list[FDA_PredicateDevice]] = Field(
        None, description="Predicate devices cited for substantial equivalence"
    )

    # Statement
    statement_or_summary: Optional[str] = Field(
        None, description="510(k) summary or statement indicator"
    )

    # Third party review
    third_party_flag: Optional[bool] = Field(
        None, description="Whether reviewed by accredited third party"
    )

    @field_validator("k_number")
    @classmethod
    def validate_k_number(cls, v: str) -> str:
        result = validate_k_number_format(v)
        if result is None:
            raise ValueError("k_number is required")
        return result

    @field_validator("date_received", "decision_date", mode="before")
    @classmethod
    def parse_dates(cls, v):
        return validate_iso_date(v)

    @computed_field
    @property
    def clearance_type(self) -> ClearanceType:
        """Determine clearance type from K number."""
        return ClearanceType.from_k_number(self.k_number)

    @computed_field
    @property
    def is_de_novo(self) -> bool:
        """Check if this is a De Novo classification."""
        return self.k_number.upper().startswith("DEN")

    @computed_field
    @property
    def is_cleared(self) -> bool:
        """Check if device was cleared (substantially equivalent)."""
        if self.decision_code:
            return self.decision_code.upper() in ("SESE", "SE")
        return self.decision_date is not None


class FDA_510kClearanceCreate(FDA_510kClearance):
    """Schema for creating a new 510(k) clearance record."""

    pass


class FDA_510kClearanceResponse(FDA_510kClearance, AuditedModel):
    """Schema for 510(k) clearance API responses with audit fields."""

    id: Optional[str] = Field(None, description="Primary key identifier")


class FDA_PMAClearance(FDA_ClearanceBase):
    """
    FDA Premarket Approval (PMA).

    PMA is the most stringent type of device marketing application
    required by FDA, typically for Class III devices.

    Reference: 21 CFR Part 814
    """

    pma_number: str = Field(
        ...,
        description="FDA-assigned PMA number (P followed by 6 digits)",
        examples=["P200001"],
    )

    # Dates
    date_received: Optional[date] = Field(
        None, description="Date FDA received the PMA submission"
    )
    decision_date: Optional[date] = Field(
        None, description="Date of FDA approval decision"
    )

    # Supplements
    supplement_number: Optional[str] = Field(
        None, description="Supplement number if this is a PMA supplement"
    )
    supplement_type: Optional[str] = Field(
        None, description="Type of PMA supplement"
    )

    @field_validator("pma_number")
    @classmethod
    def validate_pma(cls, v: str) -> str:
        result = validate_pma_number_format(v)
        if result is None:
            raise ValueError("pma_number is required")
        return result


class FDA_DeNovoClearance(FDA_ClearanceBase):
    """
    FDA De Novo Classification Request.

    De Novo provides a pathway for novel low-to-moderate risk devices
    that lack a predicate device.

    Reference: 21 CFR 860.220
    """

    de_novo_number: str = Field(
        ...,
        description="FDA-assigned De Novo number (DEN followed by 6 digits)",
        examples=["DEN180067"],
    )

    # Dates
    date_received: Optional[date] = Field(
        None, description="Date FDA received the De Novo request"
    )
    decision_date: Optional[date] = Field(
        None, description="Date of FDA decision"
    )

    # De Novo specific
    new_product_code: Optional[str] = Field(
        None,
        max_length=3,
        description="New product code established by De Novo grant",
    )
    new_regulation_number: Optional[str] = Field(
        None,
        description="New 21 CFR regulation number established",
    )

    @field_validator("de_novo_number")
    @classmethod
    def validate_den(cls, v: str) -> str:
        result = validate_k_number_format(v)  # DEN uses same format validation
        if result is None:
            raise ValueError("de_novo_number is required")
        if not result.startswith("DEN"):
            raise ValueError("De Novo number must start with 'DEN'")
        return result


# =============================================================================
# Regulatory Authorization (Generic Lifecycle Tracking)
# =============================================================================


class RegulatoryFrameworkInfo(AshMaticsBaseModel):
    """Nested schema for regulatory framework information."""

    id: int
    framework_code: str
    framework_name: str
    authorization_type: str
    regulator_code: Optional[str] = None


class ProductStatusInfo(AshMaticsBaseModel):
    """Nested schema for product regulatory status information."""

    id: int
    product_id: int
    regulator_id: int
    regulatory_status: str


class RegulatoryAuthorizationBase(AshMaticsBaseModel):
    """
    Base schema for regulatory authorizations.

    Represents specific market authorizations granted under regulatory
    frameworks (510(k), PMA, CE Mark, ARTG registration, etc.).

    Tracks authorization lifecycle including expiry and renewal.
    """

    authorization_number: str = Field(
        ...,
        max_length=100,
        description="Unique authorization number (e.g., K123456, P123456)",
    )
    authorization_date: Optional[date] = Field(
        None,
        validation_alias=AliasChoices("authorization_date", "decision_date"),
        description="Date authorization was granted (FDA: decision_date)",
    )
    effective_date: Optional[date] = Field(
        None,
        description="Date authorization became effective",
    )
    expiry_date: Optional[date] = Field(
        None,
        description="Date authorization expires (if applicable)",
    )
    renewal_due_date: Optional[date] = Field(
        None,
        description="Date renewal is due",
    )
    status: AuthorizationStatus = Field(
        ...,
        description="Authorization lifecycle status (active, expired, withdrawn, suspended, under_review)",
    )
    withdrawal_reason: Optional[str] = Field(
        None,
        description="Reason if withdrawn",
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes",
    )

    # FDA-specific fields
    date_received: Optional[date] = Field(
        None,
        description="FDA: Date Document Control Center received submission",
    )
    expedited_review_flag: Optional[bool] = Field(
        None,
        description="FDA: Whether eligible for priority/expedited review",
    )
    third_party_flag: Optional[bool] = Field(
        None,
        description="FDA: Whether eligible for third-party review",
    )


class RegulatoryAuthorizationCreate(RegulatoryAuthorizationBase):
    """Schema for creating a new regulatory authorization."""

    product_regulatory_status_id: int = Field(
        ..., gt=0, description="Foreign key to product_regulatory_status"
    )
    framework_id: int = Field(
        ..., gt=0, description="Foreign key to regulatory_frameworks"
    )
    premarket_clearance_id: Optional[str] = Field(
        None, description="Foreign key to premarket_clearances (optional)"
    )


class RegulatoryAuthorizationUpdate(AshMaticsBaseModel):
    """Schema for updating an existing regulatory authorization."""

    model_config = {"extra": "ignore"}

    authorization_number: Optional[str] = Field(None, max_length=100)
    authorization_date: Optional[date] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None
    renewal_due_date: Optional[date] = None
    status: Optional[AuthorizationStatus] = None
    withdrawal_reason: Optional[str] = None
    notes: Optional[str] = None
    date_received: Optional[date] = None
    expedited_review_flag: Optional[bool] = None
    third_party_flag: Optional[bool] = None


class RegulatoryAuthorizationResponse(RegulatoryAuthorizationBase, TimestampedModel):
    """
    Schema for regulatory authorization responses.

    Includes computed properties and nested framework/status info.
    """

    id: Optional[int] = None
    product_regulatory_status_id: int
    framework_id: int
    premarket_clearance_id: Optional[str] = None
    updated_by_id: Optional[int] = None

    # Computed properties
    is_expired: Optional[bool] = Field(None, description="Whether authorization has expired")
    days_until_expiry: Optional[int] = Field(None, description="Days until authorization expires")
    requires_renewal_soon: Optional[bool] = Field(
        None, description="Whether renewal is due within 90 days"
    )

    # Nested information
    framework: Optional[RegulatoryFrameworkInfo] = None
    product_status: Optional[ProductStatusInfo] = None


class RegulatoryAuthorizationStats(AshMaticsBaseModel):
    """Schema for regulatory authorization statistics."""

    total_authorizations: int = Field(..., description="Total number of authorizations")
    by_framework: dict[str, int] = Field(
        default_factory=dict, description="Count by framework code"
    )
    by_status: dict[str, int] = Field(
        default_factory=dict, description="Count by authorization status"
    )
    active_count: int = Field(..., description="Number of active authorizations")
    expired_count: int = Field(..., description="Number of expired authorizations")
    expiring_soon_count: int = Field(..., description="Number expiring within 90 days")
    renewal_due_count: int = Field(..., description="Number requiring renewal within 90 days")
