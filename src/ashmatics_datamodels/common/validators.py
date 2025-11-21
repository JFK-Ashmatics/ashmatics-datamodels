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
Shared validation functions for data models.

These validators can be used across jurisdiction-specific schemas
for common validation patterns.
"""

import re
from datetime import date, datetime
from typing import Optional

# ISO 3166-1 alpha-2 country codes (commonly used subset)
# Full list available at: https://www.iso.org/iso-3166-country-codes.html
VALID_COUNTRY_CODES = {
    "US",
    "CA",
    "MX",  # North America
    "GB",
    "DE",
    "FR",
    "IT",
    "ES",
    "NL",
    "BE",
    "CH",
    "AT",
    "SE",
    "NO",
    "DK",
    "FI",
    "IE",
    "PL",
    "CZ",
    "PT",  # Europe
    "CN",
    "JP",
    "KR",
    "IN",
    "AU",
    "NZ",
    "SG",
    "HK",
    "TW",
    "TH",
    "MY",
    "ID",
    "PH",
    "VN",  # Asia-Pacific
    "BR",
    "AR",
    "CL",
    "CO",
    "PE",  # Latin America
    "IL",
    "AE",
    "SA",
    "ZA",
    "EG",  # Middle East & Africa
}


def validate_country_code(value: Optional[str]) -> Optional[str]:
    """
    Validate ISO 3166-1 alpha-2 country code.

    Args:
        value: Two-letter country code (e.g., 'US', 'DE', 'JP')

    Returns:
        Uppercase country code if valid

    Raises:
        ValueError: If code is not a valid ISO 3166-1 alpha-2 code
    """
    if value is None:
        return None

    normalized = value.upper().strip()

    if len(normalized) != 2:
        raise ValueError(
            f"Invalid country code '{value}': must be exactly 2 characters"
        )

    if normalized not in VALID_COUNTRY_CODES:
        raise ValueError(
            f"Invalid ISO 3166-1 country code '{value}'. "
            f"Expected one of: {', '.join(sorted(VALID_COUNTRY_CODES))}"
        )

    return normalized


def validate_iso_date(value: Optional[str]) -> Optional[date]:
    """
    Validate and parse ISO 8601 date string.

    Args:
        value: Date string in YYYY-MM-DD format

    Returns:
        Parsed date object if valid

    Raises:
        ValueError: If date format is invalid
    """
    if value is None:
        return None

    if isinstance(value, date):
        return value

    if isinstance(value, datetime):
        return value.date()

    # Try ISO format first
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        pass

    # Try common US format
    try:
        return datetime.strptime(value, "%m/%d/%Y").date()
    except ValueError:
        pass

    raise ValueError(
        f"Invalid date format '{value}'. Expected YYYY-MM-DD or MM/DD/YYYY"
    )


def validate_k_number_format(value: Optional[str]) -> Optional[str]:
    """
    Validate FDA 510(k) number format.

    Valid formats:
        - K###### (Traditional 510(k))
        - BK###### (510(k) submitted by CBER)
        - DEN###### (De Novo)

    Args:
        value: K number string

    Returns:
        Uppercase K number if valid

    Raises:
        ValueError: If format is invalid
    """
    if value is None:
        return None

    normalized = value.upper().strip()

    # Pattern: K, BK, or DEN followed by 6-7 digits
    pattern = r"^(K|BK|DEN)\d{6,7}$"

    if not re.match(pattern, normalized):
        raise ValueError(
            f"Invalid 510(k) number format '{value}'. "
            "Expected K######, BK######, or DEN###### (6-7 digits)"
        )

    return normalized


def validate_pma_number_format(value: Optional[str]) -> Optional[str]:
    """
    Validate FDA PMA number format.

    Valid format: P###### (P followed by 6 digits)

    Args:
        value: PMA number string

    Returns:
        Uppercase PMA number if valid

    Raises:
        ValueError: If format is invalid
    """
    if value is None:
        return None

    normalized = value.upper().strip()

    pattern = r"^P\d{6}$"

    if not re.match(pattern, normalized):
        raise ValueError(
            f"Invalid PMA number format '{value}'. Expected P###### (6 digits)"
        )

    return normalized


def validate_product_code(value: Optional[str]) -> Optional[str]:
    """
    Validate FDA product code format.

    Product codes are 3-letter codes assigned by FDA to medical devices.

    Args:
        value: Product code string

    Returns:
        Uppercase product code if valid

    Raises:
        ValueError: If format is invalid
    """
    if value is None:
        return None

    normalized = value.upper().strip()

    if not re.match(r"^[A-Z]{3}$", normalized):
        raise ValueError(
            f"Invalid product code format '{value}'. Expected 3 uppercase letters"
        )

    return normalized
