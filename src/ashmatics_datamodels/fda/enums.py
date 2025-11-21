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
FDA-specific enumerations aligned with OpenFDA vocabulary.

These enums are derived from ASHKBAPP-33 work and align with
OpenFDA Device API data dictionary.

Reference: 21 CFR Parts 807, 814, 860
Vocabulary Source: OpenFDA Device API (https://open.fda.gov/device/)
"""

from enum import Enum


class ClearanceType(str, Enum):
    """
    FDA premarket clearance pathway types.

    Reference: 21 CFR Parts 807, 814, 860
    Vocabulary Source: OpenFDA Device API

    Values map to FDA regulatory submission types for medical devices.
    """

    PMA = "PMA"  # Premarket Approval (21 CFR Part 814)
    K510 = "510(k)"  # Traditional 510(k) Clearance (21 CFR Part 807)
    DE_NOVO = "De Novo"  # De Novo Classification Request (21 CFR 860.220)
    HDE = "HDE"  # Humanitarian Device Exemption (21 CFR Part 814 Subpart H)
    EUA = "EUA"  # Emergency Use Authorization (21 USC 360bbb-3)

    @classmethod
    def from_k_number(cls, k_number: str) -> "ClearanceType":
        """
        Determine clearance type from K number prefix.

        Args:
            k_number: FDA submission number (e.g., K240001, DEN180067)

        Returns:
            Appropriate ClearanceType based on prefix
        """
        k_upper = k_number.upper()
        if k_upper.startswith("K") or k_upper.startswith("BK"):
            return cls.K510
        elif k_upper.startswith("DEN"):
            return cls.DE_NOVO
        elif k_upper.startswith("P"):
            return cls.PMA
        elif k_upper.startswith("H"):
            return cls.HDE
        else:
            raise ValueError(f"Cannot determine clearance type from: {k_number}")


class FDA_DeviceClass(str, Enum):
    """
    FDA risk-based device classification.

    Reference: 21 CFR Part 860
    Risk Levels: Class I (low), Class II (moderate), Class III (high)

    Device classification determines regulatory controls and submission requirements.
    """

    CLASS_1 = "1"  # Low risk - General controls only
    CLASS_2 = "2"  # Moderate risk - General + Special controls
    CLASS_3 = "3"  # High risk - General controls + Premarket approval

    @property
    def risk_level(self) -> str:
        """Get human-readable risk level."""
        risk_map = {
            FDA_DeviceClass.CLASS_1: "Low Risk",
            FDA_DeviceClass.CLASS_2: "Moderate Risk",
            FDA_DeviceClass.CLASS_3: "High Risk",
        }
        return risk_map[self]

    @property
    def regulatory_controls(self) -> list[str]:
        """Get typical regulatory controls for this class."""
        controls = {
            FDA_DeviceClass.CLASS_1: ["General Controls"],
            FDA_DeviceClass.CLASS_2: ["General Controls", "Special Controls"],
            FDA_DeviceClass.CLASS_3: ["General Controls", "Premarket Approval"],
        }
        return controls[self]

    @property
    def typical_submission(self) -> str:
        """Get typical submission pathway for this class."""
        submissions = {
            FDA_DeviceClass.CLASS_1: "Exempt or 510(k)",
            FDA_DeviceClass.CLASS_2: "510(k)",
            FDA_DeviceClass.CLASS_3: "PMA",
        }
        return submissions[self]


class Modality(str, Enum):
    """
    Medical device modalities for imaging and diagnostic equipment.

    Maps to RADLEX ontology where applicable.
    Vocabulary Source: RADLEX (Radiology Lexicon) from RSNA
    """

    CT = "CT"  # Computed Tomography (RADLEX:RID10003)
    MR = "MR"  # Magnetic Resonance Imaging (RADLEX:RID10009)
    MG = "MG"  # Mammography (RADLEX:RID10011)
    POST = "PostProcessing"  # Image Post-Processing Systems
    US = "US"  # Ultrasound (RADLEX:RID10013)
    EEG = "EEG"  # Electroencephalography
    ECG = "ECG"  # Electrocardiography
    XR = "Xray"  # X-Ray Radiography (RADLEX:RID10345)
    XA = "Xray Angiography"  # X-Ray Angiography
    NM = "Nuclear Medicine"  # Nuclear Medicine (RADLEX:RID10330)
    PET = "PET"  # Positron Emission Tomography (RADLEX:RID10337)
    SPECT = "SPECT"  # Single-Photon Emission Computed Tomography
    PATHOLOGY = "Pathology"  # Digital pathology / whole slide imaging
    ENDOSCOPY = "Endoscopy"  # Endoscopic imaging
    OPHTHALMOLOGY = "Ophthalmology"  # Ophthalmic imaging (fundus, OCT)
    DERMATOLOGY = "Dermatology"  # Dermatoscopy and skin imaging


class SubmissionType(str, Enum):
    """
    FDA submission pathway types required for product classification.

    Reference: 21 CFR Parts 807, 814, 860
    Vocabulary Source: OpenFDA Device Classification API

    Indicates the premarket submission pathway required based on
    device classification and intended use.
    """

    K510 = "510(k)"  # 510(k) Premarket Notification required
    PMA = "PMA"  # Premarket Approval Application required
    DE_NOVO = "De Novo"  # De Novo Classification Request pathway
    EXEMPT = "Exempt"  # Exempt from premarket submission (typically Class I)
    HDE = "HDE"  # Humanitarian Device Exemption pathway
    PDP = "PDP"  # Product Development Protocol (rarely used alternative to PMA)


class ReviewPanel(str, Enum):
    """
    FDA review panel codes for device classification.

    Each medical device is assigned to a review panel based on
    its intended use and technological characteristics.

    Reference: 21 CFR Parts 862-892
    """

    AN = "AN"  # Anesthesiology
    CV = "CV"  # Cardiovascular
    CH = "CH"  # Clinical Chemistry
    DE = "DE"  # Dental
    EN = "EN"  # Ear, Nose, Throat
    GU = "GU"  # Gastroenterology/Urology
    HO = "HO"  # General Hospital
    HE = "HE"  # Hematology
    IM = "IM"  # Immunology
    MI = "MI"  # Microbiology
    NE = "NE"  # Neurology
    OB = "OB"  # Obstetrics/Gynecology
    OP = "OP"  # Ophthalmic
    OR = "OR"  # Orthopedic
    PA = "PA"  # Pathology
    PM = "PM"  # Physical Medicine
    RA = "RA"  # Radiology
    SU = "SU"  # General/Plastic Surgery
    TX = "TX"  # Clinical Toxicology
