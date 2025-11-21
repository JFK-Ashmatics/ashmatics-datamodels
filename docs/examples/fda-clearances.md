# FDA Clearances Examples

Practical examples for working with FDA clearance schemas.

## Basic 510(k) Clearance

```python
from ashmatics_datamodels.fda import (
    FDA_510kClearance,
    FDA_DeviceClass,
    ClearanceType,
)

clearance = FDA_510kClearance(
    k_number="K240001",
    device_name="AI-Powered Chest X-ray Analyzer",
    clearance_date="2024-08-15",
    device_class=FDA_DeviceClass.CLASS_2,
    applicant="Medical AI Corporation",
    clearance_type=ClearanceType.TRADITIONAL_510K,
    product_code="MYN",
    decision_description="Substantially equivalent",
)

print(f"Device: {clearance.device_name}")
print(f"K Number: {clearance.k_number}")
print(f"Class: {clearance.device_class}")
```

## Validating K Numbers

```python
from ashmatics_datamodels.fda import FDA_510kClearance
from pydantic import ValidationError

# Valid K numbers
try:
    c1 = FDA_510kClearance(k_number="K240001", device_name="Device 1")
    c2 = FDA_510kClearance(k_number="BK240002", device_name="Device 2")
    c3 = FDA_510kClearance(k_number="DEN240003", device_name="Device 3")
    print("All valid!")
except ValidationError as e:
    print(f"Validation error: {e}")

# Invalid K number
try:
    invalid = FDA_510kClearance(k_number="INVALID", device_name="Bad Device")
except ValidationError as e:
    print(f"Error: Invalid K number format")
```

## Processing OpenFDA API Data

```python
import requests
from ashmatics_datamodels.fda import FDA_510kClearance

# Fetch from OpenFDA API
response = requests.get(
    "https://api.fda.gov/device/510k.json",
    params={
        "search": "device_name:chest AND decision_date:[2024-01-01 TO 2024-12-31]",
        "limit": 10
    }
)

data = response.json()

# Parse into validated models
clearances = []
for item in data["results"]:
    try:
        clearance = FDA_510kClearance(
            k_number=item.get("k_number"),
            device_name=item.get("device_name"),
            clearance_date=item.get("decision_date"),
            applicant=item.get("applicant"),
            device_class=item.get("device_class", "2"),
            product_code=item.get("product_code"),
        )
        clearances.append(clearance)
    except Exception as e:
        print(f"Skipping invalid entry: {e}")

print(f"Parsed {len(clearances)} clearances")
```

## PMA Approval

```python
from ashmatics_datamodels.fda import FDA_PMAClearance, FDA_DeviceClass

pma = FDA_PMAClearance(
    pma_number="P240001",
    device_name="Advanced Cardiac Imaging System",
    approval_date="2024-09-01",
    applicant="CardioTech Inc",
    device_class=FDA_DeviceClass.CLASS_3,
    product_code="DXY",
    supplement_number=None,  # Original PMA
)

print(f"PMA: {pma.pma_number}")
print(f"Class: {pma.device_class}")  # Always Class III for PMA
```

## De Novo Classification

```python
from ashmatics_datamodels.fda import FDA_DeNovoClearance

denovo = FDA_DeNovoClearance(
    k_number="DEN240001",  # De Novo uses DEN prefix
    device_name="Novel AI Diagnostic Tool",
    clearance_date="2024-07-20",
    applicant="Innovation Medical Inc",
    device_class=FDA_DeviceClass.CLASS_2,  # Typically Class I or II
    product_code="ABC",
    review_panel="Radiology",
)

print(f"De Novo: {denovo.k_number}")
print(f"Review Panel: {denovo.review_panel}")
```

## Predicate Device Tracking

```python
from ashmatics_datamodels.fda import (
    FDA_510kClearance,
    FDA_PredicateDevice,
)

clearance = FDA_510kClearance(
    k_number="K240001",
    device_name="New AI Device",
    clearance_date="2024-08-15",
    applicant="Medical AI Corp",
)

# Add predicate device information
predicate = FDA_PredicateDevice(
    k_number="K190123",
    device_name="Previous AI Device",
    applicant="Competitor Inc",
    clearance_date="2019-05-10",
)

# In practice, you'd store these separately and link via k_number
print(f"New device {clearance.k_number} based on predicate {predicate.k_number}")
```

## Batch Import from CSV

```python
import csv
from ashmatics_datamodels.fda import FDA_510kClearance
from pydantic import ValidationError

clearances = []
errors = []

with open("510k_data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            clearance = FDA_510kClearance(
                k_number=row["k_number"],
                device_name=row["device_name"],
                clearance_date=row["decision_date"],
                applicant=row["applicant"],
                device_class=row.get("device_class", "2"),
            )
            clearances.append(clearance)
        except ValidationError as e:
            errors.append({
                "row": row,
                "error": str(e)
            })

print(f"Successfully imported: {len(clearances)}")
print(f"Errors: {len(errors)}")
```

## Export to JSON

```python
from ashmatics_datamodels.fda import FDA_510kClearance
import json

clearance = FDA_510kClearance(
    k_number="K240001",
    device_name="AI Device",
    clearance_date="2024-08-15",
    applicant="Medical Corp",
)

# Export to dict
data = clearance.model_dump()

# Export to JSON string
json_str = json.dumps(data, default=str, indent=2)
print(json_str)

# Save to file
with open("clearance_K240001.json", "w") as f:
    json.dump(data, f, default=str, indent=2)
```

## Querying by Date Range

```python
from ashmatics_datamodels.fda import FDA_510kClearance
from datetime import date

clearances = [
    FDA_510kClearance(k_number="K240001", clearance_date="2024-01-15"),
    FDA_510kClearance(k_number="K240002", clearance_date="2024-06-20"),
    FDA_510kClearance(k_number="K240003", clearance_date="2024-11-05"),
]

# Filter by date range
start_date = date(2024, 6, 1)
end_date = date(2024, 12, 31)

recent = [
    c for c in clearances
    if start_date <= c.clearance_date <= end_date
]

print(f"Clearances from Jun-Dec 2024: {len(recent)}")
```

## Complete Example: Build a Clearance Database

```python
import requests
from ashmatics_datamodels.fda import (
    FDA_510kClearance,
    FDA_ManufacturerBase,
)
from datetime import date

def fetch_and_parse_clearances(year: int) -> list[FDA_510kClearance]:
    """Fetch 510(k) clearances from OpenFDA for a given year."""
    clearances = []

    response = requests.get(
        "https://api.fda.gov/device/510k.json",
        params={
            "search": f"decision_date:[{year}-01-01 TO {year}-12-31]",
            "limit": 100
        }
    )

    if response.status_code != 200:
        print(f"API error: {response.status_code}")
        return clearances

    data = response.json()

    for item in data.get("results", []):
        try:
            clearance = FDA_510kClearance(
                k_number=item["k_number"],
                device_name=item.get("device_name", ""),
                clearance_date=item.get("decision_date"),
                applicant=item.get("applicant"),
                device_class=item.get("device_class"),
                product_code=item.get("product_code"),
            )
            clearances.append(clearance)
        except Exception as e:
            print(f"Skipping {item.get('k_number')}: {e}")

    return clearances

# Fetch 2024 clearances
clearances_2024 = fetch_and_parse_clearances(2024)
print(f"Fetched {len(clearances_2024)} clearances from 2024")

# Export to JSON
import json
with open("510k_2024.json", "w") as f:
    json.dump(
        [c.model_dump() for c in clearances_2024],
        f,
        default=str,
        indent=2
    )
```
