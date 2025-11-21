# fda/ Module

The `fda/` module provides FDA-specific schemas aligned with the OpenFDA API structure.

## Overview

All FDA schemas mirror the [OpenFDA API](https://open.fda.gov/) response structures for easy data integration:

- Field names match OpenFDA JSON keys
- Enums align with OpenFDA terminology
- Date formats support both ISO 8601 and US formats

## Manufacturers

### FDA_ManufacturerBase

Basic manufacturer information.

```python
from ashmatics_datamodels.fda import FDA_ManufacturerBase

manufacturer = FDA_ManufacturerBase(
    manufacturer_name="Medical AI Corporation",
    applicant="Medical AI Corporation",
)
```

### FDA_ManufacturerAddress

Contact and address information.

```python
from ashmatics_datamodels.fda import FDA_ManufacturerAddress

address = FDA_ManufacturerAddress(
    street1="123 Innovation Way",
    city="San Francisco",
    state="CA",
    zip_code="94103",
    country_code="US",
)
```

## Clearances

### FDA_510kClearance

510(k) premarket notification clearances.

```python
from ashmatics_datamodels.fda import (
    FDA_510kClearance,
    FDA_DeviceClass,
    ClearanceType,
)

clearance = FDA_510kClearance(
    k_number="K240001",
    device_name="AI-Chest Scanner",
    clearance_date="2024-08-15",
    device_class=FDA_DeviceClass.CLASS_2,
    applicant="Medical AI Corp",
    clearance_type=ClearanceType.TRADITIONAL_510K,
)
```

**K Number Formats:**
- `K######` - Traditional 510(k)
- `BK######` - 510(k) submitted by CBER
- `DEN######` - De Novo classification

### FDA_PMAClearance

PMA (Premarket Approval) clearances.

```python
from ashmatics_datamodels.fda import FDA_PMAClearance

pma = FDA_PMAClearance(
    pma_number="P240001",
    device_name="Advanced Medical Device",
    approval_date="2024-09-01",
    applicant="Medical Corp",
)
```

### FDA_DeNovoClearance

De Novo classification clearances.

```python
from ashmatics_datamodels.fda import FDA_DeNovoClearance

denovo = FDA_DeNovoClearance(
    k_number="DEN240001",  # De Novo uses DEN prefix
    device_name="Novel Device",
    clearance_date="2024-07-20",
    applicant="Innovation Inc",
)
```

## Classifications

### FDA_ProductCode

3-letter FDA product codes.

```python
from ashmatics_datamodels.fda import FDA_ProductCode, FDA_DeviceClass

product_code = FDA_ProductCode(
    product_code="MYN",
    device_name="Computer-assisted diagnostic software",
    device_class=FDA_DeviceClass.CLASS_2,
    medical_specialty="Radiology",
)
```

### FDA_DeviceClassification

Complete device classification information.

```python
from ashmatics_datamodels.fda import FDA_DeviceClassification

classification = FDA_DeviceClassification(
    product_code="MYN",
    device_class=FDA_DeviceClass.CLASS_2,
    device_name="Computer-assisted diagnostic software",
    definition="Software that analyzes medical images",
    regulation_number="21 CFR 892.2050",
)
```

## Products

Product and regulatory status tracking.

```python
from ashmatics_datamodels.fda import (
    FDA_ProductBase,
    ProductRegulatoryStatusBase,
)

product = FDA_ProductBase(
    product_name="AI-Chest Scanner",
    manufacturer_id="mfr-001",
    product_code="MYN",
    device_class=FDA_DeviceClass.CLASS_2,
)

status = ProductRegulatoryStatusBase(
    product_id="prod-001",
    regulator_id="fda",
    authorization_status=AuthorizationStatus.CLEARED,
    clearance_number="K240001",
)
```

## Recalls

FDA device recall information.

```python
from ashmatics_datamodels.fda import (
    FDA_RecallBase,
    RecallClass,
    RecallStatus,
)

recall = FDA_RecallBase(
    recall_number="Z-1234-2024",
    product_description="AI-Chest Scanner v1.0",
    reason_for_recall="Software malfunction",
    recall_class=RecallClass.CLASS_II,
    status=RecallStatus.ONGOING,
    recall_initiation_date="2024-10-15",
)
```

**Recall Classes:**
- `CLASS_I` - Serious health hazard or death
- `CLASS_II` - Temporary or reversible adverse health consequences
- `CLASS_III` - Not likely to cause adverse health consequences

## Adverse Events

MAUDE (Manufacturer and User Facility Device Experience) adverse events.

```python
from ashmatics_datamodels.fda import (
    FDA_AdverseEventBase,
    EventType,
    FDA_MAUDEDevice,
)

event = FDA_AdverseEventBase(
    report_number="1234567",
    event_date="2024-11-01",
    event_type=EventType.MALFUNCTION,
    device_info=FDA_MAUDEDevice(
        brand_name="AI-Chest Scanner",
        generic_name="Diagnostic AI Software",
        manufacturer_name="Medical AI Corp",
    ),
    event_description="Software failed to load patient data",
)
```

**Event Types:**
- `DEATH` - Patient death
- `INJURY` - Patient injury
- `MALFUNCTION` - Device malfunction only
- `OTHER` - Other events

## Enums

### ClearanceType

```python
from ashmatics_datamodels.fda.enums import ClearanceType

# Values:
# TRADITIONAL_510K
# SPECIAL_510K
# ABBREVIATED_510K
# PMA
# DE_NOVO
```

### FDA_DeviceClass

```python
from ashmatics_datamodels.fda.enums import FDA_DeviceClass

# Values:
# CLASS_1 - Low risk
# CLASS_2 - Moderate risk
# CLASS_3 - High risk
```

### Modality

Imaging modalities for diagnostic devices.

```python
from ashmatics_datamodels.fda.enums import Modality

# Values: X_RAY, CT, MRI, ULTRASOUND, MAMMOGRAPHY, etc.
```

## File Reference

| File | Purpose |
|------|---------|
| `manufacturers.py` | Manufacturer schemas |
| `clearances.py` | 510(k), PMA, De Novo clearances |
| `classifications.py` | Product codes and classifications |
| `products.py` | Product and regulatory status |
| `recalls.py` | Recall information |
| `adverse_events.py` | MAUDE adverse event reports |
| `enums.py` | FDA-specific enumerations |

## OpenFDA Integration

Example of processing OpenFDA API data:

```python
import requests
from ashmatics_datamodels.fda import FDA_510kClearance

# Fetch from OpenFDA
response = requests.get(
    "https://api.fda.gov/device/510k.json",
    params={"search": "k_number:K240001"}
)
data = response.json()["results"][0]

# Parse into validated model
clearance = FDA_510kClearance(
    k_number=data["k_number"],
    device_name=data["device_name"],
    clearance_date=data["decision_date"],
    applicant=data["applicant"],
)
```

## Complete API Reference

For detailed API documentation, see [API Reference: fda](../api/fda.md).
