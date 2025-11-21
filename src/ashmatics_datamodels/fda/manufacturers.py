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
FDA Manufacturer schemas using OpenFDA vocabulary.

These schemas are designed for direct mapping from OpenFDA API responses.

Vocabulary Source: https://open.fda.gov/device/510k/
Reference: 21 CFR Part 807 (Registration and Listing)
"""

from typing import Optional

from pydantic import Field, computed_field, field_validator

from ashmatics_datamodels.common.base import AshMaticsBaseModel, AuditedModel
from ashmatics_datamodels.common.validators import validate_country_code


class FDA_ManufacturerAddress(AshMaticsBaseModel):
    """
    Manufacturer address using FDA vocabulary.

    Field names match OpenFDA Device API exactly for direct mapping.

    Vocabulary Source: https://open.fda.gov/device/
    Fields: manufacturer_address_1, manufacturer_address_2, manufacturer_city,
            manufacturer_state, manufacturer_postal_code, manufacturer_country
    """

    manufacturer_address_1: Optional[str] = Field(
        None,
        max_length=255,
        description="Primary address line (street number and name)",
    )
    manufacturer_address_2: Optional[str] = Field(
        None,
        max_length=255,
        description="Secondary address line (suite, building, etc.)",
    )
    manufacturer_city: Optional[str] = Field(
        None, max_length=100, description="City name"
    )
    manufacturer_state: Optional[str] = Field(
        None,
        max_length=50,
        description="State/province code or name",
    )
    manufacturer_postal_code: Optional[str] = Field(
        None,
        max_length=20,
        description="Postal code (US ZIP code or international equivalent)",
    )
    manufacturer_country: Optional[str] = Field(
        None,
        max_length=2,
        description="ISO 3166-1 alpha-2 country code (e.g., 'US', 'DE', 'JP')",
    )

    @field_validator("manufacturer_country")
    @classmethod
    def validate_country(cls, v: Optional[str]) -> Optional[str]:
        """Validate ISO country code."""
        return validate_country_code(v)


class FDA_ManufacturerBase(AshMaticsBaseModel):
    """
    Base FDA manufacturer schema.

    Vocabulary Source: https://open.fda.gov/device/510k/
    FDA Definition: The manufacturer of record or entity responsible for the device.

    Key Distinction:
    - manufacturer_name: Entity that manufactures the device
    - applicant: Entity that submits the 510(k) (may differ from manufacturer)
    """

    manufacturer_name: str = Field(
        ...,
        max_length=255,
        description="Name of the entity that manufactures the device",
    )

    applicant: Optional[str] = Field(
        None,
        max_length=255,
        description=(
            "Entity that submits the 510(k) premarket notification. "
            "May be the manufacturer, a third party, or consultant. "
            "After Aug 14, 2014, typically the manufacturer."
        ),
    )

    # FDA facility identifiers
    fei_number: Optional[list[str]] = Field(
        None,
        description=(
            "Facility Establishment Identifier assigned by FDA Office of Regulatory Affairs. "
            "Format: 10-digit number. May have multiple if manufacturer has multiple facilities."
        ),
    )

    registration_number: Optional[list[str]] = Field(
        None, description="FDA facility registration number(s)"
    )

    # Contact information
    contact_name: Optional[str] = Field(
        None, max_length=255, description="Primary contact person name"
    )
    contact_email: Optional[str] = Field(
        None, max_length=255, description="Contact email address"
    )
    contact_phone: Optional[str] = Field(
        None, max_length=50, description="Contact phone number"
    )

    # Address (nested)
    address: Optional[FDA_ManufacturerAddress] = Field(
        None, description="Manufacturer address in FDA vocabulary format"
    )

    # Company metadata
    website: Optional[str] = Field(
        None, max_length=255, description="Company website URL"
    )


class FDA_ManufacturerCreate(FDA_ManufacturerBase):
    """Schema for creating a new FDA manufacturer record."""

    pass


class FDA_ManufacturerResponse(FDA_ManufacturerBase, AuditedModel):
    """
    Schema for FDA manufacturer responses.

    Includes audit fields and computed properties for common queries.
    """

    id: Optional[str] = Field(None, description="Primary key identifier")

    @computed_field
    @property
    def is_us_based(self) -> bool:
        """Check if manufacturer is US-based."""
        if self.address and self.address.manufacturer_country:
            return self.address.manufacturer_country.upper() == "US"
        return False

    @computed_field
    @property
    def applicant_is_manufacturer(self) -> bool:
        """Check if applicant and manufacturer are the same entity."""
        if self.applicant is None:
            return True  # Assume same if not specified
        # Normalize and compare
        return self.applicant.strip().lower() == self.manufacturer_name.strip().lower()

    @computed_field
    @property
    def display_name(self) -> str:
        """Get display name (applicant if different, else manufacturer)."""
        if self.applicant and not self.applicant_is_manufacturer:
            return f"{self.manufacturer_name} (via {self.applicant})"
        return self.manufacturer_name
