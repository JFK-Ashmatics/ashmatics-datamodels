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

"""Tests for FDA clearance schemas."""

import pytest
from datetime import date

from ashmatics_datamodels.fda import (
    FDA_510kClearance,
    FDA_DeviceClass,
    ClearanceType,
)


class TestFDA510kClearance:
    """Tests for FDA_510kClearance schema."""

    def test_valid_510k_clearance(self):
        """Test creating a valid 510(k) clearance."""
        clearance = FDA_510kClearance(
            k_number="K240001",
            device_name="AI-Chest Scanner",
            device_class=FDA_DeviceClass.CLASS_2,
            decision_date="2024-08-15",
        )

        assert clearance.k_number == "K240001"
        assert clearance.device_name == "AI-Chest Scanner"
        assert clearance.device_class == FDA_DeviceClass.CLASS_2
        assert clearance.decision_date == date(2024, 8, 15)

    def test_k_number_uppercase_normalization(self):
        """Test that K numbers are normalized to uppercase."""
        clearance = FDA_510kClearance(
            k_number="k240001",
            device_name="Test Device",
        )
        assert clearance.k_number == "K240001"

    def test_clearance_type_computed(self):
        """Test that clearance type is computed from K number."""
        k510 = FDA_510kClearance(k_number="K240001", device_name="Device 1")
        assert k510.clearance_type == ClearanceType.K510

        de_novo = FDA_510kClearance(k_number="DEN180067", device_name="Device 2")
        assert de_novo.clearance_type == ClearanceType.DE_NOVO
        assert de_novo.is_de_novo is True

    def test_invalid_k_number_format(self):
        """Test validation rejects invalid K number formats."""
        with pytest.raises(ValueError, match="Invalid 510\\(k\\) number format"):
            FDA_510kClearance(
                k_number="INVALID123",
                device_name="Test Device",
            )

    def test_is_cleared_computed(self):
        """Test is_cleared computed property."""
        # Cleared device
        cleared = FDA_510kClearance(
            k_number="K240001",
            device_name="Cleared Device",
            decision_code="SESE",
        )
        assert cleared.is_cleared is True

        # Not substantially equivalent
        nse = FDA_510kClearance(
            k_number="K240002",
            device_name="NSE Device",
            decision_code="NSE",
        )
        assert nse.is_cleared is False

    def test_date_parsing_iso_format(self):
        """Test date parsing from ISO format."""
        clearance = FDA_510kClearance(
            k_number="K240001",
            device_name="Test",
            date_received="2024-01-15",
            decision_date="2024-08-15",
        )
        assert clearance.date_received == date(2024, 1, 15)
        assert clearance.decision_date == date(2024, 8, 15)

    def test_predicate_devices(self):
        """Test predicate devices list."""
        from ashmatics_datamodels.fda.clearances import FDA_PredicateDevice

        predicate = FDA_PredicateDevice(
            k_number="K190123",
            device_name="ChestView AI",
            manufacturer="Competing AI Inc",
        )

        clearance = FDA_510kClearance(
            k_number="K240001",
            device_name="AI-Chest Scanner",
            predicate_devices=[predicate],
        )

        assert len(clearance.predicate_devices) == 1
        assert clearance.predicate_devices[0].k_number == "K190123"


class TestClearanceType:
    """Tests for ClearanceType enum."""

    def test_from_k_number(self):
        """Test determining clearance type from K number."""
        assert ClearanceType.from_k_number("K240001") == ClearanceType.K510
        assert ClearanceType.from_k_number("BK200001") == ClearanceType.K510
        assert ClearanceType.from_k_number("DEN180067") == ClearanceType.DE_NOVO
        assert ClearanceType.from_k_number("P200001") == ClearanceType.PMA
        assert ClearanceType.from_k_number("H200001") == ClearanceType.HDE

    def test_invalid_prefix(self):
        """Test that invalid prefix raises error."""
        with pytest.raises(ValueError, match="Cannot determine clearance type"):
            ClearanceType.from_k_number("X123456")


class TestFDADeviceClass:
    """Tests for FDA_DeviceClass enum."""

    def test_risk_level_property(self):
        """Test risk level computed property."""
        assert FDA_DeviceClass.CLASS_1.risk_level == "Low Risk"
        assert FDA_DeviceClass.CLASS_2.risk_level == "Moderate Risk"
        assert FDA_DeviceClass.CLASS_3.risk_level == "High Risk"

    def test_regulatory_controls(self):
        """Test regulatory controls property."""
        assert "General Controls" in FDA_DeviceClass.CLASS_1.regulatory_controls
        assert "Special Controls" in FDA_DeviceClass.CLASS_2.regulatory_controls
        assert "Premarket Approval" in FDA_DeviceClass.CLASS_3.regulatory_controls

    def test_typical_submission(self):
        """Test typical submission pathway property."""
        assert "Exempt" in FDA_DeviceClass.CLASS_1.typical_submission
        assert FDA_DeviceClass.CLASS_2.typical_submission == "510(k)"
        assert FDA_DeviceClass.CLASS_3.typical_submission == "PMA"
