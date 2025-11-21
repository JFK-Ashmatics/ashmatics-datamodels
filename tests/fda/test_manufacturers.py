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

"""Tests for FDA manufacturer schemas."""

import pytest

from ashmatics_datamodels.fda import (
    FDA_ManufacturerBase,
    FDA_ManufacturerResponse,
    FDA_ManufacturerAddress,
)


class TestFDAManufacturerAddress:
    """Tests for FDA_ManufacturerAddress schema."""

    def test_valid_us_address(self):
        """Test creating a valid US address."""
        address = FDA_ManufacturerAddress(
            manufacturer_address_1="710 Medtronic Parkway",
            manufacturer_city="Minneapolis",
            manufacturer_state="MN",
            manufacturer_postal_code="55432",
            manufacturer_country="US",
        )

        assert address.manufacturer_city == "Minneapolis"
        assert address.manufacturer_country == "US"

    def test_country_code_uppercase(self):
        """Test that country code is normalized to uppercase."""
        address = FDA_ManufacturerAddress(manufacturer_country="us")
        assert address.manufacturer_country == "US"

    def test_invalid_country_code(self):
        """Test validation rejects invalid country codes."""
        # "USA" is 3 chars, caught by max_length before validator
        with pytest.raises((ValueError, Exception), match="too_long|Invalid"):
            FDA_ManufacturerAddress(manufacturer_country="USA")

    def test_unknown_country_code(self):
        """Test validation rejects unknown 2-letter codes."""
        with pytest.raises((ValueError, Exception), match="Invalid ISO"):
            FDA_ManufacturerAddress(manufacturer_country="XX")


class TestFDAManufacturerBase:
    """Tests for FDA_ManufacturerBase schema."""

    def test_minimal_manufacturer(self):
        """Test creating manufacturer with only required fields."""
        manufacturer = FDA_ManufacturerBase(manufacturer_name="Medical AI Corp")

        assert manufacturer.manufacturer_name == "Medical AI Corp"
        assert manufacturer.applicant is None
        assert manufacturer.fei_number is None

    def test_full_manufacturer(self):
        """Test creating manufacturer with all fields."""
        manufacturer = FDA_ManufacturerBase(
            manufacturer_name="Medtronic, Inc.",
            applicant="Medtronic, Inc.",
            fei_number=["1234567890", "0987654321"],
            registration_number=["REG123"],
            contact_name="John Doe",
            contact_email="john.doe@medtronic.com",
            website="https://www.medtronic.com",
            address=FDA_ManufacturerAddress(
                manufacturer_address_1="710 Medtronic Parkway",
                manufacturer_city="Minneapolis",
                manufacturer_state="MN",
                manufacturer_country="US",
            ),
        )

        assert manufacturer.manufacturer_name == "Medtronic, Inc."
        assert len(manufacturer.fei_number) == 2
        assert manufacturer.address.manufacturer_city == "Minneapolis"


class TestFDAManufacturerResponse:
    """Tests for FDA_ManufacturerResponse schema with computed properties."""

    def test_is_us_based_true(self):
        """Test is_us_based returns True for US manufacturers."""
        manufacturer = FDA_ManufacturerResponse(
            manufacturer_name="US Corp",
            address=FDA_ManufacturerAddress(manufacturer_country="US"),
        )
        assert manufacturer.is_us_based is True

    def test_is_us_based_false(self):
        """Test is_us_based returns False for non-US manufacturers."""
        manufacturer = FDA_ManufacturerResponse(
            manufacturer_name="German Corp",
            address=FDA_ManufacturerAddress(manufacturer_country="DE"),
        )
        assert manufacturer.is_us_based is False

    def test_applicant_is_manufacturer_same(self):
        """Test when applicant matches manufacturer."""
        manufacturer = FDA_ManufacturerResponse(
            manufacturer_name="Medical AI Corp",
            applicant="Medical AI Corp",
        )
        assert manufacturer.applicant_is_manufacturer is True

    def test_applicant_is_manufacturer_different(self):
        """Test when applicant differs from manufacturer."""
        manufacturer = FDA_ManufacturerResponse(
            manufacturer_name="Subsidiary Inc",
            applicant="Parent Corporation",
        )
        assert manufacturer.applicant_is_manufacturer is False

    def test_display_name_same_entity(self):
        """Test display name when applicant is manufacturer."""
        manufacturer = FDA_ManufacturerResponse(
            manufacturer_name="Medical AI Corp",
            applicant="Medical AI Corp",
        )
        assert manufacturer.display_name == "Medical AI Corp"

    def test_display_name_different_entity(self):
        """Test display name when applicant differs."""
        manufacturer = FDA_ManufacturerResponse(
            manufacturer_name="Subsidiary Inc",
            applicant="Parent Corporation",
        )
        assert "via Parent Corporation" in manufacturer.display_name


class TestOpenFDAMapping:
    """Test direct mapping from OpenFDA API response format."""

    def test_openfda_address_mapping(self):
        """Test that OpenFDA JSON maps directly to schema."""
        # Simulated OpenFDA API response fields
        openfda_data = {
            "manufacturer_address_1": "100 Abbott Park Road",
            "manufacturer_city": "Abbott Park",
            "manufacturer_state": "IL",
            "manufacturer_postal_code": "60064",
            "manufacturer_country": "US",
        }

        address = FDA_ManufacturerAddress(**openfda_data)
        assert address.manufacturer_city == "Abbott Park"
        assert address.manufacturer_state == "IL"

    def test_openfda_manufacturer_mapping(self):
        """Test full manufacturer mapping from OpenFDA format."""
        openfda_data = {
            "manufacturer_name": "Abbott Laboratories",
            "applicant": "Abbott Laboratories",
            "fei_number": ["1234567890"],
        }

        manufacturer = FDA_ManufacturerBase(**openfda_data)
        assert manufacturer.manufacturer_name == "Abbott Laboratories"
