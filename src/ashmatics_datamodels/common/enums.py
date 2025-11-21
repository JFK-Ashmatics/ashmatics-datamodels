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
Common enumerations shared across jurisdictions.

These enums represent concepts that are jurisdiction-agnostic or
shared across multiple regulatory frameworks.
"""

from enum import Enum


class AuthorizationStatus(str, Enum):
    """
    Lifecycle status of regulatory authorizations.

    Workflow: UNDER_REVIEW → ACTIVE → {EXPIRED | WITHDRAWN | SUSPENDED}

    Used for tracking state of 510(k) clearances, PMA approvals,
    CE Marks, and other regulatory authorizations.

    Reference: ASHMATICS Workflow Ontology
    """

    ACTIVE = "active"  # Authorization currently valid and in effect
    EXPIRED = "expired"  # Authorization past expiry date, no longer valid
    WITHDRAWN = "withdrawn"  # Authorization voluntarily withdrawn by holder
    SUSPENDED = "suspended"  # Authorization temporarily suspended by authority
    UNDER_REVIEW = "under_review"  # Application under regulatory review


class RegulatoryStatus(str, Enum):
    """
    Overall regulatory standing of a product across jurisdictions.

    Workflow: PENDING → {APPROVED | REJECTED}
    Post-Market: APPROVED → {WITHDRAWN | SUSPENDED}

    Represents product-level regulatory status, distinct from
    individual authorization status.

    Reference: ASHMATICS Workflow Ontology
    """

    APPROVED = "approved"  # Product has received regulatory approval
    PENDING = "pending"  # Product submission under regulatory review
    REJECTED = "rejected"  # Product submission rejected by authority
    WITHDRAWN = "withdrawn"  # Product voluntarily withdrawn from market
    SUSPENDED = "suspended"  # Product marketing suspended by authority


class RiskCategory(str, Enum):
    """
    General risk categorization for medical devices.

    Maps to FDA Device Class: Low (I), Moderate (II), High (III)

    Used for risk-based filtering and analysis across regulatory
    jurisdictions. Aligns with FDA device classification system.

    Reference: ASHMATICS Risk Ontology
    """

    LOW = "low"  # Minimal potential for harm (Class I devices)
    MODERATE = "moderate"  # Moderate potential requiring special controls (Class II)
    HIGH = "high"  # Significant potential for harm (Class III)


class ParsingStatus(str, Enum):
    """
    Document parsing workflow status.

    Workflow: PENDING → IN_PROGRESS → {COMPLETED | FAILED}
    Alternative: PENDING → SKIPPED

    Used for tracking AI-powered document processing, chunking,
    and knowledge graph extraction workflows.

    Reference: ASHMATICS Internal Workflow Ontology
    """

    PENDING = "pending"  # Document queued for parsing
    IN_PROGRESS = "in_progress"  # Document currently being processed
    COMPLETED = "completed"  # Document successfully parsed
    FAILED = "failed"  # Document parsing encountered errors
    SKIPPED = "skipped"  # Document intentionally not parsed


class Region(str, Enum):
    """
    Geographic regions for manufacturer categorization.

    Maps to ISO 3166-1 country codes where applicable, with custom
    regional groupings (EU, APAC, LATAM).
    """

    USA = "USA"
    EU = "EU"
    DE = "DE"
    UK = "UK"
    CHINA = "CHINA"
    APAC = "APAC"
    LATAM = "LATAM"
    AUS = "AUS"
    JP = "JP"
    KR = "KR"
    OTHER = "OTHER"
