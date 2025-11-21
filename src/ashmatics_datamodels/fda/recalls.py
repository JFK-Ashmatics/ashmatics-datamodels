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
FDA Device Recall schemas.

Aligned with OpenFDA Device Recall API for tracking device recalls,
corrections, and removals.

Reference: 21 CFR Part 7 (Enforcement Policy)
Vocabulary Source: https://open.fda.gov/device/recall/
"""

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import Field

from ashmatics_datamodels.common.base import AshMaticsBaseModel, TimestampedModel


class RecallStatus(str, Enum):
    """FDA recall status values."""

    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    TERMINATED = "Terminated"
    PENDING = "Pending"


class RecallClass(str, Enum):
    """
    FDA recall classification based on health hazard severity.

    Class I: Most serious - reasonable probability of serious adverse health consequences or death
    Class II: May cause temporary or reversible adverse health consequences
    Class III: Not likely to cause adverse health consequences
    """

    CLASS_I = "Class I"
    CLASS_II = "Class II"
    CLASS_III = "Class III"


class RecallType(str, Enum):
    """Type of recall action."""

    RECALL = "Recall"
    CORRECTION = "Correction"
    REMOVAL = "Removal"
    MARKET_WITHDRAWAL = "Market Withdrawal"


class FDA_RecallBase(AshMaticsBaseModel):
    """
    Base schema for FDA device recalls.

    Represents a recall, correction, or removal action for a medical device.
    """

    # Recall identification
    recall_number: str = Field(
        ...,
        max_length=50,
        description="FDA-assigned recall number (e.g., Z-1234-2024)",
    )
    event_id: Optional[str] = Field(
        None,
        max_length=50,
        description="FDA event ID linking related recalls",
    )

    # Classification
    recall_class: Optional[RecallClass] = Field(
        None,
        description="Recall classification (I, II, III) based on health hazard",
    )
    recall_status: Optional[RecallStatus] = Field(
        None,
        description="Current status of the recall",
    )
    recall_type: Optional[RecallType] = Field(
        None,
        description="Type of recall action",
    )

    # Device information
    product_description: str = Field(
        ...,
        description="Description of the recalled product",
    )
    product_code: Optional[str] = Field(
        None,
        max_length=3,
        description="FDA three-letter product code",
    )
    k_numbers: Optional[list[str]] = Field(
        None,
        description="Associated 510(k) numbers",
    )
    pma_numbers: Optional[list[str]] = Field(
        None,
        description="Associated PMA numbers",
    )

    # Firm information
    recalling_firm: str = Field(
        ...,
        max_length=255,
        description="Name of the firm conducting the recall",
    )
    firm_fei_number: Optional[str] = Field(
        None,
        max_length=20,
        description="FDA Establishment Identifier of recalling firm",
    )

    # Recall details
    reason_for_recall: Optional[str] = Field(
        None,
        description="Reason for the recall",
    )
    root_cause_description: Optional[str] = Field(
        None,
        description="Root cause of the issue",
    )
    action: Optional[str] = Field(
        None,
        description="Action being taken (e.g., 'repair', 'replace', 'refund')",
    )

    # Distribution
    distribution_pattern: Optional[str] = Field(
        None,
        description="Geographic distribution of affected products",
    )
    product_quantity: Optional[str] = Field(
        None,
        description="Quantity of products affected",
    )

    # Dates
    recall_initiation_date: Optional[date] = Field(
        None,
        description="Date recall was initiated by firm",
    )
    center_classification_date: Optional[date] = Field(
        None,
        description="Date FDA classified the recall",
    )
    termination_date: Optional[date] = Field(
        None,
        description="Date recall was terminated (if applicable)",
    )

    # Additional context
    additional_info_contact: Optional[str] = Field(
        None,
        description="Contact information for additional details",
    )
    code_info: Optional[str] = Field(
        None,
        description="Product codes, lot numbers, serial numbers affected",
    )


class FDA_RecallCreate(FDA_RecallBase):
    """Schema for creating a new recall record."""

    pass


class FDA_RecallResponse(FDA_RecallBase, TimestampedModel):
    """Schema for recall API responses."""

    id: Optional[str] = Field(None, description="Record identifier")

    # Computed/linked fields
    related_clearances_count: int = Field(
        0, description="Number of linked clearances"
    )
    adverse_events_count: int = Field(
        0, description="Number of related adverse events"
    )


class FDA_RecallStats(AshMaticsBaseModel):
    """Schema for recall statistics."""

    total_recalls: int = Field(..., description="Total number of recalls")
    by_class: dict[str, int] = Field(
        default_factory=dict, description="Count by recall class"
    )
    by_status: dict[str, int] = Field(
        default_factory=dict, description="Count by recall status"
    )
    by_year: dict[str, int] = Field(
        default_factory=dict, description="Count by initiation year"
    )
    class_i_count: int = Field(0, description="Number of Class I (most serious) recalls")
    ongoing_count: int = Field(0, description="Number of ongoing recalls")
