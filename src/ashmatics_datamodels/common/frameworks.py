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
Regulatory Framework schemas for multi-jurisdiction support.

Regulatory frameworks represent specific approval pathways within
each jurisdiction (510(k), PMA, CE Mark, ARTG, etc.).

Migrated from: KB src/app/schemas/regulatory_framework_schema.py
JIRA: ASHKBAPP-28 (Phase 2.1)
"""

from datetime import datetime
from typing import Optional

from pydantic import Field

from ashmatics_datamodels.common.base import AshMaticsBaseModel, TimestampedModel
from ashmatics_datamodels.common.regulators import RegulatorSummary


class RegulatoryFrameworkBase(AshMaticsBaseModel):
    """
    Base schema for regulatory frameworks.

    A regulatory framework represents a specific pathway for device
    authorization (e.g., FDA 510(k), FDA PMA, EU CE Mark, TGA ARTG).
    """

    framework_code: str = Field(
        ...,
        max_length=50,
        description="Unique framework code (e.g., '510K', 'PMA', 'CE_MARK', 'ARTG')",
    )
    framework_name: str = Field(
        ...,
        max_length=255,
        description="Full framework name (e.g., 'Premarket Notification 510(k)')",
    )
    authorization_type: str = Field(
        ...,
        max_length=50,
        description="Type: clearance, approval, registration, notification, self_certification",
    )
    requires_premarket_review: bool = Field(
        ...,
        description="Whether premarket review by regulator is required",
    )
    requires_clinical_data: bool = Field(
        False,
        description="Whether clinical data submission is required",
    )
    description: Optional[str] = Field(
        None,
        description="Detailed framework description",
    )
    typical_review_time_days: Optional[int] = Field(
        None,
        ge=0,
        description="Typical review time in days",
    )
    renewal_required: bool = Field(
        False,
        description="Whether periodic renewal is required",
    )
    renewal_frequency_years: Optional[int] = Field(
        None,
        ge=1,
        description="Renewal frequency in years (if applicable)",
    )
    is_active: bool = Field(
        True,
        description="Whether framework is currently active",
    )


class RegulatoryFrameworkCreate(RegulatoryFrameworkBase):
    """Schema for creating a new regulatory framework."""

    regulator_id: int = Field(
        ...,
        gt=0,
        description="Foreign key to regulators",
    )


class RegulatoryFrameworkUpdate(AshMaticsBaseModel):
    """Schema for updating an existing regulatory framework."""

    model_config = {"extra": "ignore"}

    framework_name: Optional[str] = Field(None, max_length=255)
    authorization_type: Optional[str] = Field(None, max_length=50)
    requires_premarket_review: Optional[bool] = None
    requires_clinical_data: Optional[bool] = None
    description: Optional[str] = None
    typical_review_time_days: Optional[int] = None
    renewal_required: Optional[bool] = None
    renewal_frequency_years: Optional[int] = None
    is_active: Optional[bool] = None


class RegulatoryFrameworkResponse(RegulatoryFrameworkBase, TimestampedModel):
    """
    Schema for regulatory framework responses.

    Includes nested regulator information and computed fields.
    """

    id: Optional[int] = Field(None, description="Framework ID")
    regulator_id: int = Field(..., description="Foreign key to regulators")

    # Nested regulator information
    regulator: Optional[RegulatorSummary] = Field(
        None, description="Regulator details"
    )

    # Computed fields
    authorization_count: int = Field(
        0, description="Number of authorizations under this framework"
    )


class RegulatoryFrameworkSummary(AshMaticsBaseModel):
    """Minimal framework information for nested responses."""

    id: int
    framework_code: str
    framework_name: str
    authorization_type: str
    regulator_code: Optional[str] = None


class RegulatoryFrameworkStats(AshMaticsBaseModel):
    """Schema for regulatory framework statistics."""

    total_frameworks: int = Field(..., description="Total number of frameworks")
    active_frameworks: int = Field(..., description="Number of active frameworks")
    by_authorization_type: dict[str, int] = Field(
        default_factory=dict, description="Count by authorization type"
    )
    by_regulator: dict[str, int] = Field(
        default_factory=dict, description="Count by regulator"
    )
    requiring_premarket_review: int = Field(
        0, description="Frameworks requiring premarket review"
    )
    requiring_clinical_data: int = Field(
        0, description="Frameworks requiring clinical data"
    )
    requiring_renewal: int = Field(
        0, description="Frameworks requiring periodic renewal"
    )
    avg_review_time_days: Optional[float] = Field(
        None, description="Average review time in days"
    )
