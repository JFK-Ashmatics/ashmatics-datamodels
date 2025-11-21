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
Use Case Category schemas for hierarchical taxonomy.

Provides hierarchical categorization for organizing clinical AI use cases.
Derived from ASHKBAPP-28 Phase 2.3 work.
"""

from datetime import datetime
from typing import Optional

from pydantic import Field

from ashmatics_datamodels.common.base import AshMaticsBaseModel, TimestampedModel


class UseCaseCategoryBase(AshMaticsBaseModel):
    """
    Base schema for use case category data.

    Contains core fields common across create, update, and response operations.
    """

    category_name: str = Field(
        ..., max_length=255, description="Human-readable category name"
    )
    category_code: str = Field(
        ..., max_length=50, description="Unique category code (e.g., 'RAD_CHEST')"
    )
    description: Optional[str] = Field(
        None, description="Detailed category description"
    )
    display_order: int = Field(
        0, description="Order for display within parent category"
    )
    is_active: bool = Field(True, description="Whether category is currently active")


class UseCaseCategoryCreate(UseCaseCategoryBase):
    """
    Schema for creating a new use case category.

    Includes optional parent_category_id for hierarchical structure.
    """

    parent_category_id: Optional[int] = Field(
        None, gt=0, description="Foreign key to parent category (None for top-level)"
    )


class UseCaseCategoryUpdate(AshMaticsBaseModel):
    """
    Schema for updating an existing use case category.

    All fields are optional to support partial updates.
    """

    category_name: Optional[str] = Field(None, max_length=255)
    category_code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    parent_category_id: Optional[int] = Field(None, gt=0)
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class UseCaseCategoryResponse(UseCaseCategoryBase, TimestampedModel):
    """
    Schema for use case category responses.

    Includes all fields plus metadata and nested children.
    """

    id: int
    parent_category_id: Optional[int] = None

    # Computed properties
    is_top_level: Optional[bool] = Field(
        None, description="Whether this is a top-level category"
    )
    full_path: Optional[str] = Field(
        None, description="Full category path (e.g., 'Clinical Specialties > Radiology')"
    )

    # Nested children (for tree view)
    children: Optional[list["UseCaseCategoryResponse"]] = Field(
        None, description="Child categories"
    )


class UseCaseCategoryTree(AshMaticsBaseModel):
    """
    Schema for hierarchical tree view of categories.
    """

    top_level_categories: list[UseCaseCategoryResponse] = Field(
        ..., description="Top-level categories with nested children"
    )
    total_categories: int = Field(
        ..., description="Total number of categories in tree"
    )
    max_depth: int = Field(
        ..., description="Maximum depth of category hierarchy"
    )
