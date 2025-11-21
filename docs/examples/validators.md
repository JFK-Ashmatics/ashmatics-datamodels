# Validators Examples

Examples using the common validation functions.

## K Number Validation

```python
from ashmatics_datamodels.common.validators import validate_k_number_format

# Valid K numbers
k1 = validate_k_number_format("K240001")    # Returns "K240001"
k2 = validate_k_number_format("k240001")    # Returns "K240001" (normalized)
k3 = validate_k_number_format("BK240001")   # Returns "BK240001" (CBER)
k4 = validate_k_number_format("DEN240001")  # Returns "DEN240001" (De Novo)

# Invalid format raises ValueError
try:
    invalid = validate_k_number_format("INVALID")
except ValueError as e:
    print(f"Error: {e}")
    # Error: Invalid 510(k) number format 'INVALID'...
```

## Date Validation

```python
from ashmatics_datamodels.common.validators import validate_iso_date
from datetime import date

# ISO 8601 format
d1 = validate_iso_date("2024-08-15")  # Returns date(2024, 8, 15)

# US format
d2 = validate_iso_date("08/15/2024")  # Returns date(2024, 8, 15)

# Already a date object
d3 = validate_iso_date(date(2024, 8, 15))  # Returns date(2024, 8, 15)

# Invalid format
try:
    invalid = validate_iso_date("15-08-2024")
except ValueError as e:
    print(f"Error: {e}")
```

## Product Code Validation

```python
from ashmatics_datamodels.common.validators import validate_product_code

# Valid 3-letter codes
code1 = validate_product_code("MYN")  # Returns "MYN"
code2 = validate_product_code("myn")  # Returns "MYN" (normalized)

# Invalid codes
try:
    validate_product_code("MY")     # Too short
except ValueError:
    print("Code too short")

try:
    validate_product_code("MYNA")   # Too long
except ValueError:
    print("Code too long")
```

## Country Code Validation

```python
from ashmatics_datamodels.common.validators import validate_country_code

# Valid ISO 3166-1 alpha-2 codes
c1 = validate_country_code("US")  # Returns "US"
c2 = validate_country_code("us")  # Returns "US" (normalized)
c3 = validate_country_code("GB")  # Returns "GB"

# Invalid code
try:
    validate_country_code("USA")  # 3-letter code
except ValueError:
    print("Invalid code")
```

## PMA Number Validation

```python
from ashmatics_datamodels.common.validators import validate_pma_number_format

# Valid PMA numbers (P followed by 6 digits)
pma1 = validate_pma_number_format("P240001")  # Returns "P240001"
pma2 = validate_pma_number_format("p240001")  # Returns "P240001"

# Invalid format
try:
    validate_pma_number_format("PMA240001")
except ValueError:
    print("Invalid format")
```

## Using Validators in Pydantic Models

```python
from pydantic import field_validator
from ashmatics_datamodels.common import AshMaticsBaseModel
from ashmatics_datamodels.common.validators import (
    validate_k_number_format,
    validate_product_code,
)

class MyDevice(AshMaticsBaseModel):
    k_number: str
    product_code: str

    @field_validator("k_number")
    @classmethod
    def validate_k_number(cls, v):
        return validate_k_number_format(v)

    @field_validator("product_code")
    @classmethod
    def validate_product_code_field(cls, v):
        return validate_product_code(v)

# Valid device
device = MyDevice(k_number="k240001", product_code="myn")
print(device.k_number)      # "K240001" (normalized)
print(device.product_code)  # "MYN" (normalized)

# Invalid device
try:
    bad_device = MyDevice(k_number="INVALID", product_code="myn")
except Exception as e:
    print(f"Validation error: {e}")
```
