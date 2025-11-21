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
FDA vocabulary schemas aligned with OpenFDA Device API.

This module provides Pydantic models for:
- Manufacturers and applicants
- 510(k) clearances, PMA approvals, De Novo classifications
- Device classifications and product codes
- FDA-specific enumerations

Vocabulary Source: https://open.fda.gov/device/
Reference: 21 CFR Parts 807, 814, 860
"""

from ashmatics_datamodels.fda.clearances import (
    FDA_510kClearance,
    FDA_510kClearanceCreate,
    FDA_ClearanceBase,
    FDA_DeNovoClearance,
    FDA_PMAClearance,
)
from ashmatics_datamodels.fda.classifications import (
    FDA_DeviceClassification,
    FDA_ProductCode,
)
from ashmatics_datamodels.fda.enums import (
    ClearanceType,
    FDA_DeviceClass,
    Modality,
    SubmissionType,
)
from ashmatics_datamodels.fda.manufacturers import (
    FDA_ManufacturerAddress,
    FDA_ManufacturerBase,
    FDA_ManufacturerCreate,
    FDA_ManufacturerResponse,
)

__all__ = [
    # Enums
    "ClearanceType",
    "FDA_DeviceClass",
    "Modality",
    "SubmissionType",
    # Manufacturers
    "FDA_ManufacturerAddress",
    "FDA_ManufacturerBase",
    "FDA_ManufacturerCreate",
    "FDA_ManufacturerResponse",
    # Clearances
    "FDA_ClearanceBase",
    "FDA_510kClearance",
    "FDA_510kClearanceCreate",
    "FDA_PMAClearance",
    "FDA_DeNovoClearance",
    # Classifications
    "FDA_DeviceClassification",
    "FDA_ProductCode",
]
