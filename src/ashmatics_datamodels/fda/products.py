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
FDA Product and Regulatory Status schemas.

Includes:
- FDA_ProductBase: Core product/device information
- ProductRegulatoryStatus: Per-jurisdiction regulatory standing

Migrated from: KB src/app/schemas/product_regulatory_status_schema.py
JIRA: ASHKBAPP-28 (Phase 2.3)
"""

from datetime import date, datetime
from typing import Optional

from pydantic import Field

from ashmatics_datamodels.common.base import AshMaticsBaseModel, TimestampedModel
from ashmatics_datamodels.common.enums import RegulatoryStatus


# =============================================================================
# Core Product Schemas
# =============================================================================


class FDA_ProductBase(AshMaticsBaseModel):
    """
    Base schema for FDA medical device products.

    Represents a marketed medical device with basic identification
    and manufacturer information.
    """

    product_name: str = Field(
        ...,
        max_length=500,
        description="Official product name",
    )
    manufacturer_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Manufacturer name",
    )
    brand_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Brand name as used in labeling",
    )
    generic_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Common/generic name of the device",
    )
    catalog_number: Optional[str] = Field(
        None,
        max_length=100,
        description="Manufacturer's catalog/model number",
    )
    device_description: Optional[str] = Field(
        None,
        description="Description of the device",
    )
    intended_use: Optional[str] = Field(
        None,
        description="Intended use statement",
    )
    is_active: bool = Field(
        True,
        description="Whether product is currently marketed",
    )


class FDA_ProductCreate(FDA_ProductBase):
    """Schema for creating a new product."""

    manufacturer_id: Optional[int] = Field(
        None,
        gt=0,
        description="Foreign key to manufacturers table",
    )


class FDA_ProductResponse(FDA_ProductBase, TimestampedModel):
    """Schema for product responses."""

    id: Optional[int] = Field(None, description="Product ID")
    manufacturer_id: Optional[int] = Field(None, description="Foreign key to manufacturer")

    # Computed/derived fields
    clearance_count: int = Field(0, description="Number of associated clearances")
    regulatory_status_count: int = Field(
        0, description="Number of jurisdictions with regulatory status"
    )


# =============================================================================
# Product Regulatory Status (Per-Jurisdiction Standing)
# =============================================================================


class RegulatorInfo(AshMaticsBaseModel):
    """Nested schema for regulator information."""

    id: int
    code: str
    name: str
    region: Optional[str] = None


class ClassificationInfo(AshMaticsBaseModel):
    """Nested schema for classification information."""

    id: int
    code: str
    description: str
    device_class: Optional[str] = None
    system_code: Optional[str] = None


class ProductInfo(AshMaticsBaseModel):
    """Nested schema for product information."""

    id: int
    product_name: str
    manufacturer_name: Optional[str] = None


class ProductRegulatoryStatusBase(AshMaticsBaseModel):
    """
    Base schema for product regulatory status.

    Tracks a product's regulatory standing with a specific regulatory
    authority (FDA, EMA, TGA, etc.).
    """

    regulatory_status: RegulatoryStatus = Field(
        ...,
        description="Product regulatory status (approved, pending, rejected, withdrawn, suspended)",
    )
    status_date: Optional[date] = Field(
        None,
        description="Date when status was determined",
    )
    status_reason: Optional[str] = Field(
        None,
        description="Reason for the status",
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes",
    )
    is_active: bool = Field(
        True,
        description="Whether this status record is active",
    )


class ProductRegulatoryStatusCreate(ProductRegulatoryStatusBase):
    """Schema for creating a new product regulatory status."""

    product_id: int = Field(..., gt=0, description="Foreign key to products")
    regulator_id: int = Field(..., gt=0, description="Foreign key to regulators")
    classification_id: Optional[int] = Field(
        None, gt=0, description="Foreign key to product_classifications (optional)"
    )


class ProductRegulatoryStatusUpdate(AshMaticsBaseModel):
    """Schema for updating an existing product regulatory status."""

    model_config = {"extra": "ignore"}

    regulatory_status: Optional[RegulatoryStatus] = Field(
        None, description="Product regulatory status"
    )
    classification_id: Optional[int] = Field(None, gt=0, description="Classification ID")
    status_date: Optional[date] = Field(None, description="Status date")
    status_reason: Optional[str] = Field(None, description="Status reason")
    notes: Optional[str] = Field(None, description="Notes")
    is_active: Optional[bool] = Field(None, description="Active status")


class ProductRegulatoryStatusResponse(ProductRegulatoryStatusBase, TimestampedModel):
    """
    Schema for product regulatory status responses.

    Includes nested regulator, classification, and product info.
    """

    id: Optional[int] = None
    product_id: int
    regulator_id: int
    classification_id: Optional[int] = None
    updated_by_id: Optional[int] = None

    # Nested information
    regulator: Optional[RegulatorInfo] = None
    classification: Optional[ClassificationInfo] = None
    product: Optional[ProductInfo] = None


class ProductRegulatoryStatusStats(AshMaticsBaseModel):
    """Schema for product regulatory status statistics."""

    total_statuses: int = Field(..., description="Total number of status records")
    total_products: int = Field(..., description="Number of unique products with statuses")
    by_regulator: dict[str, int] = Field(
        default_factory=dict, description="Count by regulator code"
    )
    by_status: dict[str, int] = Field(
        default_factory=dict, description="Count by regulatory status"
    )
    active_count: int = Field(..., description="Number of active status records")
    inactive_count: int = Field(..., description="Number of inactive status records")
