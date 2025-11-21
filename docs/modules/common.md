# common/ Module

The `common/` module provides cross-jurisdictional base models, validators, enums, and utilities that are used throughout the library.

## Base Models

### AshMaticsBaseModel

The foundation for all data models in the library.

```python
from ashmatics_datamodels.common import AshMaticsBaseModel

class MyModel(AshMaticsBaseModel):
    name: str
    value: int
```

**Features:**
- `use_enum_values=True` - Serializes enums as their values
- `validate_assignment=True` - Validates when fields are assigned
- Consistent JSON serialization behavior

### TimestampedModel

Automatically tracks creation and update timestamps.

```python
from ashmatics_datamodels.common import TimestampedModel
from datetime import datetime

class Product(TimestampedModel):
    name: str
    # created_at: datetime (auto-generated)
    # updated_at: datetime (auto-updated)

product = Product(name="Test Device")
print(product.created_at)  # Current UTC timestamp
```

### AuditedModel

Full audit trail with user tracking.

```python
from ashmatics_datamodels.common import AuditedModel

class Document(AuditedModel):
    title: str
    # created_at, updated_at (from TimestampedModel)
    # created_by, updated_by (from AuditedModel)

doc = Document(title="Test", created_by="user@example.com")
```

## Validators

### validate_country_code()

Validates ISO 3166-1 alpha-2 country codes.

```python
from ashmatics_datamodels.common.validators import validate_country_code

# Valid codes
validate_country_code("US")  # "US"
validate_country_code("us")  # "US" (normalized)

# Invalid code
validate_country_code("USA")  # Raises ValueError
```

**Supported codes:** US, CA, GB, DE, FR, JP, CN, and [50+ more](../../api/common.md#validators)

### validate_iso_date()

Validates and parses date strings.

```python
from ashmatics_datamodels.common.validators import validate_iso_date

# ISO 8601 format
validate_iso_date("2024-08-15")  # date(2024, 8, 15)

# US format
validate_iso_date("08/15/2024")  # date(2024, 8, 15)

# Invalid format
validate_iso_date("15-08-2024")  # Raises ValueError
```

### validate_k_number_format()

Validates FDA 510(k) number formats.

```python
from ashmatics_datamodels.common.validators import validate_k_number_format

# Valid formats
validate_k_number_format("K240001")    # "K240001"
validate_k_number_format("BK240001")   # "BK240001" (CBER)
validate_k_number_format("DEN240001")  # "DEN240001" (De Novo)

# Invalid format
validate_k_number_format("INVALID")  # Raises ValueError
```

### validate_pma_number_format()

Validates FDA PMA number format.

```python
from ashmatics_datamodels.common.validators import validate_pma_number_format

validate_pma_number_format("P240001")  # "P240001"
validate_pma_number_format("p240001")  # "P240001" (normalized)
```

### validate_product_code()

Validates FDA product codes (3-letter codes).

```python
from ashmatics_datamodels.common.validators import validate_product_code

validate_product_code("MYN")  # "MYN"
validate_product_code("myn")  # "MYN" (normalized)
```

## Enums

### AuthorizationStatus

Regulatory authorization status.

```python
from ashmatics_datamodels.common.enums import AuthorizationStatus

status = AuthorizationStatus.CLEARED
# Values: CLEARED, APPROVED, DENIED, WITHDRAWN, PENDING
```

### RegulatoryStatus

Overall regulatory status.

```python
from ashmatics_datamodels.common.enums import RegulatoryStatus

status = RegulatoryStatus.ACTIVE
# Values: ACTIVE, INACTIVE, WITHDRAWN, SUSPENDED
```

### RiskCategory

Device risk categorization.

```python
from ashmatics_datamodels.common.enums import RiskCategory

risk = RiskCategory.MODERATE
# Values: LOW, MODERATE, HIGH
```

### Region

Geographic regions for regulatory jurisdictions.

```python
from ashmatics_datamodels.common.enums import Region

region = Region.NORTH_AMERICA
# Values: NORTH_AMERICA, EUROPE, ASIA_PACIFIC, LATIN_AMERICA,
#         MIDDLE_EAST, AFRICA, GLOBAL
```

## Regulators

Multi-jurisdiction regulator schemas.

```python
from ashmatics_datamodels.common import RegulatorBase, Region

regulator = RegulatorBase(
    name="Food and Drug Administration",
    abbreviation="FDA",
    country_code="US",
    region=Region.NORTH_AMERICA,
    website="https://www.fda.gov",
    contact_email="info@fda.gov",
)
```

**Schemas:**
- `RegulatorBase` - Base regulator information
- `RegulatorCreate` - For creating new regulators
- `RegulatorUpdate` - For updating regulators
- `RegulatorResponse` - API response format
- `RegulatorSummary` - Lightweight summary
- `RegulatorStats` - Statistics view

## Regulatory Frameworks

Regulatory framework schemas (FDA, EMA, PMDA, etc.).

```python
from ashmatics_datamodels.common import RegulatoryFrameworkBase

framework = RegulatoryFrameworkBase(
    name="510(k) Premarket Notification",
    abbreviation="510(k)",
    regulator_id="fda-001",
    description="Premarket submission to FDA demonstrating substantial equivalence",
    framework_type="clearance",
)
```

**Schemas:**
- `RegulatoryFrameworkBase` - Base framework information
- `RegulatoryFrameworkCreate` - For creating frameworks
- `RegulatoryFrameworkUpdate` - For updating frameworks
- `RegulatoryFrameworkResponse` - API response format
- `RegulatoryFrameworkSummary` - Lightweight summary
- `RegulatoryFrameworkStats` - Statistics view

## File Reference

| File | Purpose |
|------|---------|
| `base.py` | Base model classes |
| `enums.py` | Global enumerations |
| `validators.py` | Validation functions |
| `regulators.py` | Regulator schemas |
| `frameworks.py` | Regulatory framework schemas |

## Complete API Reference

For detailed API documentation, see [API Reference: common](../api/common.md).
