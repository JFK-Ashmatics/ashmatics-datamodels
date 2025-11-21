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
- Regulatory authorizations and lifecycle tracking
- Device classifications and product codes
- Products and regulatory status
- FDA-specific enumerations

Vocabulary Source: https://open.fda.gov/device/
Reference: 21 CFR Parts 807, 814, 860
"""

from ashmatics_datamodels.fda.clearances import (
    FDA_510kClearance,
    FDA_510kClearanceCreate,
    FDA_510kClearanceResponse,
    FDA_ClearanceBase,
    FDA_DeNovoClearance,
    FDA_PMAClearance,
    FDA_PredicateDevice,
    RegulatoryAuthorizationBase,
    RegulatoryAuthorizationCreate,
    RegulatoryAuthorizationResponse,
    RegulatoryAuthorizationStats,
    RegulatoryAuthorizationUpdate,
)
from ashmatics_datamodels.fda.classifications import (
    ClassificationSystemInfo,
    FDA_DeviceClassification,
    FDA_ProductCode,
    ProductClassificationBase,
    ProductClassificationCreate,
    ProductClassificationResponse,
    ProductClassificationSystemBase,
    ProductClassificationSystemCreate,
    ProductClassificationSystemResponse,
)
from ashmatics_datamodels.fda.enums import (
    ClearanceType,
    FDA_DeviceClass,
    Modality,
    ReviewPanel,
    SubmissionType,
)
from ashmatics_datamodels.fda.manufacturers import (
    FDA_ManufacturerAddress,
    FDA_ManufacturerBase,
    FDA_ManufacturerCreate,
    FDA_ManufacturerResponse,
)
from ashmatics_datamodels.fda.products import (
    FDA_ProductBase,
    FDA_ProductCreate,
    FDA_ProductResponse,
    ProductRegulatoryStatusBase,
    ProductRegulatoryStatusCreate,
    ProductRegulatoryStatusResponse,
    ProductRegulatoryStatusStats,
    ProductRegulatoryStatusUpdate,
)
from ashmatics_datamodels.fda.recalls import (
    FDA_RecallBase,
    FDA_RecallCreate,
    FDA_RecallResponse,
    FDA_RecallStats,
    RecallClass,
    RecallStatus,
    RecallType,
)
from ashmatics_datamodels.fda.adverse_events import (
    DeviceOperator,
    EventType,
    FDA_AdverseEventBase,
    FDA_AdverseEventCreate,
    FDA_AdverseEventResponse,
    FDA_AdverseEventStats,
    FDA_MAUDEDevice,
    FDA_MAUDEPatient,
    ReportSourceCode,
)

__all__ = [
    # Enums
    "ClearanceType",
    "FDA_DeviceClass",
    "Modality",
    "SubmissionType",
    "ReviewPanel",
    # Manufacturers
    "FDA_ManufacturerAddress",
    "FDA_ManufacturerBase",
    "FDA_ManufacturerCreate",
    "FDA_ManufacturerResponse",
    # Clearances (510k, PMA, De Novo)
    "FDA_ClearanceBase",
    "FDA_510kClearance",
    "FDA_510kClearanceCreate",
    "FDA_510kClearanceResponse",
    "FDA_PMAClearance",
    "FDA_DeNovoClearance",
    "FDA_PredicateDevice",
    # Regulatory Authorizations
    "RegulatoryAuthorizationBase",
    "RegulatoryAuthorizationCreate",
    "RegulatoryAuthorizationUpdate",
    "RegulatoryAuthorizationResponse",
    "RegulatoryAuthorizationStats",
    # Classifications (OpenFDA)
    "FDA_DeviceClassification",
    "FDA_ProductCode",
    # Classification Systems (Multi-jurisdiction)
    "ProductClassificationSystemBase",
    "ProductClassificationSystemCreate",
    "ProductClassificationSystemResponse",
    "ClassificationSystemInfo",
    # Product Classifications
    "ProductClassificationBase",
    "ProductClassificationCreate",
    "ProductClassificationResponse",
    # Products
    "FDA_ProductBase",
    "FDA_ProductCreate",
    "FDA_ProductResponse",
    # Product Regulatory Status
    "ProductRegulatoryStatusBase",
    "ProductRegulatoryStatusCreate",
    "ProductRegulatoryStatusUpdate",
    "ProductRegulatoryStatusResponse",
    "ProductRegulatoryStatusStats",
    # Recalls
    "FDA_RecallBase",
    "FDA_RecallCreate",
    "FDA_RecallResponse",
    "FDA_RecallStats",
    "RecallStatus",
    "RecallClass",
    "RecallType",
    # Adverse Events (MAUDE)
    "FDA_AdverseEventBase",
    "FDA_AdverseEventCreate",
    "FDA_AdverseEventResponse",
    "FDA_AdverseEventStats",
    "FDA_MAUDEDevice",
    "FDA_MAUDEPatient",
    "EventType",
    "ReportSourceCode",
    "DeviceOperator",
]
