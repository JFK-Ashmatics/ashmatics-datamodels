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
FDA MAUDE (Manufacturer and User Facility Device Experience) schemas.

Aligned with OpenFDA Device Event API for tracking adverse events
and medical device reports (MDRs).

Reference: 21 CFR Part 803 (Medical Device Reporting)
Vocabulary Source: https://open.fda.gov/device/event/
"""

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import Field

from ashmatics_datamodels.common.base import AshMaticsBaseModel, TimestampedModel


class EventType(str, Enum):
    """Type of adverse event."""

    MALFUNCTION = "Malfunction"
    INJURY = "Injury"
    DEATH = "Death"
    OTHER = "Other"
    NO_ANSWER_PROVIDED = "No answer provided"


class ReportSourceCode(str, Enum):
    """Source of the MDR report."""

    MANUFACTURER = "Manufacturer report"
    USER_FACILITY = "User facility report"
    DISTRIBUTOR = "Distributor report"
    VOLUNTARY = "Voluntary report"
    IMPORTER = "Importer report"


class DeviceOperator(str, Enum):
    """Who was operating the device when the event occurred."""

    HEALTH_PROFESSIONAL = "Health Professional"
    LAY_USER = "Lay User/Patient"
    OTHER = "Other"
    UNKNOWN = "Unknown"
    NOT_APPLICABLE = "Not Applicable"


class FDA_MAUDEDevice(AshMaticsBaseModel):
    """
    Device information within a MAUDE report.

    A single adverse event report may involve multiple devices.
    """

    brand_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Brand name of the device",
    )
    generic_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Generic/common name of the device",
    )
    manufacturer_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Device manufacturer name",
    )
    model_number: Optional[str] = Field(
        None,
        max_length=100,
        description="Model number",
    )
    catalog_number: Optional[str] = Field(
        None,
        max_length=100,
        description="Catalog number",
    )
    lot_number: Optional[str] = Field(
        None,
        max_length=100,
        description="Lot/batch number",
    )
    device_sequence_number: Optional[str] = Field(
        None,
        description="Sequence number within the report",
    )

    # Classification
    product_code: Optional[str] = Field(
        None,
        max_length=3,
        description="FDA three-letter product code",
    )
    device_class: Optional[str] = Field(
        None,
        max_length=1,
        description="Device class (1, 2, or 3)",
    )

    # Device problem
    device_problem_codes: Optional[list[str]] = Field(
        None,
        description="FDA device problem codes",
    )
    device_availability: Optional[str] = Field(
        None,
        description="Whether device was returned to manufacturer",
    )
    device_evaluated_by_manufacturer: Optional[str] = Field(
        None,
        description="Whether manufacturer evaluated the device",
    )

    # Operator
    device_operator: Optional[DeviceOperator] = Field(
        None,
        description="Who was operating the device",
    )


class FDA_MAUDEPatient(AshMaticsBaseModel):
    """
    Patient information within a MAUDE report.

    Patient-identifiable information is redacted by FDA.
    """

    patient_sequence_number: Optional[str] = Field(
        None,
        description="Sequence number within the report",
    )
    date_received: Optional[date] = Field(
        None,
        description="Date patient information was received",
    )

    # Outcome
    patient_problems: Optional[list[str]] = Field(
        None,
        description="Patient problem codes",
    )
    sequence_number_outcome: Optional[list[str]] = Field(
        None,
        description="Patient outcome codes",
    )


class FDA_AdverseEventBase(AshMaticsBaseModel):
    """
    Base schema for FDA MAUDE adverse event reports.

    Represents a Medical Device Report (MDR) submitted to FDA.
    """

    # Report identification
    mdr_report_key: str = Field(
        ...,
        description="Unique MDR report key",
    )
    report_number: Optional[str] = Field(
        None,
        max_length=50,
        description="MDR report number",
    )
    event_key: Optional[str] = Field(
        None,
        description="Event key linking related reports",
    )

    # Event classification
    event_type: Optional[EventType] = Field(
        None,
        description="Type of adverse event",
    )
    report_source_code: Optional[ReportSourceCode] = Field(
        None,
        description="Source of the report",
    )

    # Dates
    date_received: Optional[date] = Field(
        None,
        description="Date FDA received the report",
    )
    date_of_event: Optional[date] = Field(
        None,
        description="Date the event occurred",
    )
    date_report: Optional[date] = Field(
        None,
        description="Date the report was created",
    )
    date_manufacturer_received: Optional[date] = Field(
        None,
        description="Date manufacturer received information",
    )

    # Reporter information
    reporter_occupation_code: Optional[str] = Field(
        None,
        description="Occupation code of the reporter",
    )
    initial_report_to_fda: Optional[str] = Field(
        None,
        description="Whether this is the initial report to FDA",
    )

    # Event description
    event_description: Optional[str] = Field(
        None,
        description="Narrative description of the event (may be redacted)",
    )
    manufacturer_narrative: Optional[str] = Field(
        None,
        description="Manufacturer's narrative about the event",
    )

    # Manufacturer info
    manufacturer_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Manufacturer name from the report",
    )
    manufacturer_country: Optional[str] = Field(
        None,
        max_length=2,
        description="Manufacturer country code",
    )

    # Linked data
    devices: Optional[list[FDA_MAUDEDevice]] = Field(
        None,
        description="Devices involved in the event",
    )
    patients: Optional[list[FDA_MAUDEPatient]] = Field(
        None,
        description="Patients involved in the event",
    )

    # Flags
    adverse_event_flag: Optional[str] = Field(
        None,
        description="Whether classified as adverse event (Y/N)",
    )
    product_problem_flag: Optional[str] = Field(
        None,
        description="Whether there was a product problem (Y/N)",
    )
    report_to_fda: Optional[str] = Field(
        None,
        description="Whether reported to FDA (Y/N)",
    )
    report_to_manufacturer: Optional[str] = Field(
        None,
        description="Whether reported to manufacturer (Y/N)",
    )


class FDA_AdverseEventCreate(FDA_AdverseEventBase):
    """Schema for creating a new adverse event record."""

    pass


class FDA_AdverseEventResponse(FDA_AdverseEventBase, TimestampedModel):
    """Schema for adverse event API responses."""

    id: Optional[str] = Field(None, description="Record identifier")

    # Computed/linked fields
    device_count: int = Field(0, description="Number of devices in report")
    patient_count: int = Field(0, description="Number of patients in report")
    related_recalls_count: int = Field(0, description="Number of related recalls")


class FDA_AdverseEventStats(AshMaticsBaseModel):
    """Schema for adverse event statistics."""

    total_events: int = Field(..., description="Total number of events")
    by_event_type: dict[str, int] = Field(
        default_factory=dict, description="Count by event type"
    )
    by_source: dict[str, int] = Field(
        default_factory=dict, description="Count by report source"
    )
    by_year: dict[str, int] = Field(
        default_factory=dict, description="Count by event year"
    )
    deaths_count: int = Field(0, description="Number of death events")
    injuries_count: int = Field(0, description="Number of injury events")
    malfunctions_count: int = Field(0, description="Number of malfunction events")
