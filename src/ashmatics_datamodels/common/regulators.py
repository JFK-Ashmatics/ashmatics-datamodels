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
Regulator schemas for multi-jurisdiction support.

Regulators are the governing bodies that oversee medical device approval
in their respective jurisdictions (FDA, EMA, TGA, MHRA, etc.).

Migrated from: KB src/app/schemas/regulator_schema.py
JIRA: ASHKBAPP-28 (Phase 2.1)
"""

from datetime import datetime
from typing import Optional

from pydantic import Field, HttpUrl, field_validator

from ashmatics_datamodels.common.base import AshMaticsBaseModel, TimestampedModel
from ashmatics_datamodels.common.validators import validate_country_code


class RegulatorBase(AshMaticsBaseModel):
    """
    Base schema for regulatory authorities.

    Represents governing bodies like FDA (US), EMA (EU), TGA (Australia),
    MHRA (UK), Health Canada, PMDA (Japan), etc.
    """

    code: str = Field(
        ...,
        max_length=20,
        description="Regulator code (e.g., FDA, EMA, TGA, MHRA, PMDA)",
    )
    name: str = Field(
        ...,
        max_length=255,
        description="Short official name (e.g., 'Food and Drug Administration')",
    )
    full_name: Optional[str] = Field(
        None,
        max_length=500,
        description="Complete official name",
    )
    country_code: Optional[str] = Field(
        None,
        max_length=2,
        description="ISO 3166-1 alpha-2 country code (e.g., 'US', 'DE')",
    )
    region: Optional[str] = Field(
        None,
        max_length=50,
        description="Geographic region (e.g., 'North America', 'EU', 'Asia-Pacific')",
    )
    website: Optional[str] = Field(
        None,
        max_length=500,
        description="Official website URL",
    )
    api_endpoint: Optional[str] = Field(
        None,
        max_length=500,
        description="API endpoint for data integration (e.g., OpenFDA)",
    )
    is_active: bool = Field(
        True,
        description="Whether regulator is currently active",
    )

    @field_validator("country_code")
    @classmethod
    def validate_country(cls, v: Optional[str]) -> Optional[str]:
        return validate_country_code(v)


class RegulatorCreate(RegulatorBase):
    """Schema for creating a new regulator."""

    pass


class RegulatorUpdate(AshMaticsBaseModel):
    """Schema for updating an existing regulator (all fields optional)."""

    model_config = {"extra": "ignore"}  # Allow partial updates

    code: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=255)
    full_name: Optional[str] = Field(None, max_length=500)
    country_code: Optional[str] = Field(None, max_length=2)
    region: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = None
    api_endpoint: Optional[str] = None
    is_active: Optional[bool] = None


class RegulatorResponse(RegulatorBase, TimestampedModel):
    """
    Schema for regulator responses.

    Includes computed fields for framework and classification counts.
    """

    id: Optional[int] = Field(None, description="Regulator ID")

    # Computed fields (populated by endpoint logic)
    framework_count: int = Field(
        0, description="Number of regulatory frameworks under this regulator"
    )
    classification_system_count: int = Field(
        0, description="Number of classification systems managed"
    )


class RegulatorSummary(AshMaticsBaseModel):
    """Minimal regulator information for nested responses."""

    id: int
    code: str
    name: str
    region: Optional[str] = None


class RegulatorStats(AshMaticsBaseModel):
    """Schema for regulator statistics."""

    total_regulators: int = Field(..., description="Total number of regulators")
    active_regulators: int = Field(..., description="Number of active regulators")
    by_region: dict[str, int] = Field(
        default_factory=dict, description="Count by region"
    )
    by_country: dict[str, int] = Field(
        default_factory=dict, description="Count by country code"
    )
    with_frameworks: int = Field(
        0, description="Regulators with at least one framework"
    )
    with_classification_systems: int = Field(
        0, description="Regulators with at least one classification system"
    )
