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
Use Case related enumerations.

Controlled vocabularies for clinical AI use case classification.
"""

from enum import Enum


class ClinicalDomain(str, Enum):
    """
    High-level clinical domain classification.

    Used for broad categorization of clinical AI applications.
    """

    RADIOLOGY = "radiology"
    PATHOLOGY = "pathology"
    CARDIOLOGY = "cardiology"
    OPHTHALMOLOGY = "ophthalmology"
    DERMATOLOGY = "dermatology"
    ONCOLOGY = "oncology"
    NEUROLOGY = "neurology"
    GASTROENTEROLOGY = "gastroenterology"
    PULMONOLOGY = "pulmonology"
    EMERGENCY_MEDICINE = "emergency_medicine"
    PRIMARY_CARE = "primary_care"
    SURGERY = "surgery"
    CLINICAL_OPERATIONS = "clinical_operations"
    LABORATORY = "laboratory"
    OTHER = "other"


class ClinicalSpecialty(str, Enum):
    """
    Medical specialty for use case targeting.

    More granular than ClinicalDomain for specific specialty workflows.
    """

    # Radiology subspecialties
    NEURORADIOLOGY = "neuroradiology"
    MUSCULOSKELETAL_RADIOLOGY = "musculoskeletal_radiology"
    BREAST_IMAGING = "breast_imaging"
    ABDOMINAL_RADIOLOGY = "abdominal_radiology"
    THORACIC_RADIOLOGY = "thoracic_radiology"
    INTERVENTIONAL_RADIOLOGY = "interventional_radiology"
    PEDIATRIC_RADIOLOGY = "pediatric_radiology"

    # Pathology subspecialties
    SURGICAL_PATHOLOGY = "surgical_pathology"
    CYTOPATHOLOGY = "cytopathology"
    HEMATOPATHOLOGY = "hematopathology"
    DERMATOPATHOLOGY = "dermatopathology"

    # Other specialties
    CARDIOLOGY = "cardiology"
    OPHTHALMOLOGY = "ophthalmology"
    DERMATOLOGY = "dermatology"
    GASTROENTEROLOGY = "gastroenterology"
    PULMONOLOGY = "pulmonology"
    NEUROLOGY = "neurology"
    EMERGENCY_MEDICINE = "emergency_medicine"

    # General
    GENERAL = "general"
    OTHER = "other"


class DeploymentModel(str, Enum):
    """
    Deployment model for clinical AI solutions.
    """

    CLOUD = "cloud"
    ON_PREMISE = "on_premise"
    HYBRID = "hybrid"
    EDGE = "edge"  # Device-based processing


class IntegrationTarget(str, Enum):
    """
    Healthcare IT systems for integration.
    """

    PACS = "PACS"  # Picture Archiving and Communication System
    RIS = "RIS"  # Radiology Information System
    EHR = "EHR"  # Electronic Health Record
    EMR = "EMR"  # Electronic Medical Record (often used interchangeably with EHR)
    LIS = "LIS"  # Laboratory Information System
    WORKLIST = "worklist"
    VIEWER = "viewer"
    VNA = "VNA"  # Vendor Neutral Archive
    FHIR = "FHIR"  # FHIR-based integration
    HL7 = "HL7"  # HL7 v2 messaging
    DICOM = "DICOM"  # DICOM services
    OTHER = "other"


class EvidenceStrength(str, Enum):
    """
    Strength of clinical evidence supporting a use case.

    Based on standard evidence hierarchy.
    """

    STRONG = "strong"  # RCT, meta-analysis, systematic review
    MODERATE = "moderate"  # Cohort studies, case-control
    LIMITED = "limited"  # Case series, case reports
    EMERGING = "emerging"  # Pre-prints, preliminary studies
    THEORETICAL = "theoretical"  # Expert opinion, no clinical studies


class UseCaseStatus(str, Enum):
    """
    Curation status of use case content.
    """

    DRAFT = "draft"
    IN_REVIEW = "in_review"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"
