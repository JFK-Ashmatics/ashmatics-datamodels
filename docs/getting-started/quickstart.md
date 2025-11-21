# Quick Start Guide

This guide will walk you through the basic usage of AshMatics Core DataModels.

## Basic Usage

### Working with FDA Clearances

```python
from ashmatics_datamodels.fda import (
    FDA_510kClearance,
    FDA_DeviceClass,
    ClearanceType,
)

# Create a 510(k) clearance
clearance = FDA_510kClearance(
    k_number="K240001",
    device_name="AI-Powered Chest X-ray Analyzer",
    clearance_date="2024-08-15",
    device_class=FDA_DeviceClass.CLASS_2,
    applicant="Medical AI Corporation",
    clearance_type=ClearanceType.TRADITIONAL_510K,
)

# Access validated fields
print(clearance.k_number)  # "K240001"
print(clearance.device_class)  # FDA_DeviceClass.CLASS_2

# Export to JSON
json_data = clearance.model_dump(by_alias=True)
```

### Working with Manufacturers

```python
from ashmatics_datamodels.fda import (
    FDA_ManufacturerBase,
    FDA_ManufacturerAddress,
)

# Create a manufacturer with address
manufacturer = FDA_ManufacturerBase(
    manufacturer_name="Medical AI Corporation",
    applicant="Medical AI Corporation",
    contact_info=FDA_ManufacturerAddress(
        street1="123 Innovation Way",
        city="San Francisco",
        state="CA",
        zip_code="94103",
        country_code="US",
    ),
)

print(manufacturer.manufacturer_name)  # "Medical AI Corporation"
```

### Working with Product Classifications

```python
from ashmatics_datamodels.fda import (
    FDA_ProductCode,
    FDA_DeviceClass,
)

# Create a product code
product = FDA_ProductCode(
    product_code="MYN",
    device_name="Computer-assisted diagnostic software",
    device_class=FDA_DeviceClass.CLASS_2,
    medical_specialty="Radiology",
)

print(product.product_code)  # "MYN"
```

## MongoDB Document Schema

### Creating Evidence Documents

```python
from ashmatics_datamodels.documents import (
    EvidenceDocument,
    EvidenceMetadataContent,
    DocumentType,
    ContentType,
    SectionBase,
)
from datetime import date

# Create an evidence document with three-tier structure
doc = EvidenceDocument(
    _id="evidence-2024-001",
    metadata_content=EvidenceMetadataContent(
        document_type=DocumentType.EVIDENCE_DOC,
        content_type=ContentType.PEER_REVIEWED_PAPER,
        title="Deep Learning for Chest X-ray Pneumonia Detection",
        authors=["Dr. Jane Smith", "Dr. John Doe"],
        journal="Radiology: Artificial Intelligence",
        doi="10.1148/ryai.2024123456",
        publication_date=date(2024, 3, 15),
        clinical_domain="radiology",
        anatomical_region="chest",
        pathology_focus=["pneumonia", "pleural_effusion"],
        abstract="This study evaluates a deep learning model...",
    ),
)

# Add content sections
doc.content.sections["1_introduction"] = SectionBase(
    title="Introduction",
    order=1,
    text="Pneumonia is a leading cause of...",
)

# Export to MongoDB-compatible JSON
mongo_doc = doc.model_dump(by_alias=True)
```

### Creating Regulatory Documents

```python
from ashmatics_datamodels.documents import (
    RegulatoryDocument,
    RegulatoryMetadataContent,
    PredicateDeviceInfo,
)

# Create a 510(k) summary document
reg_doc = RegulatoryDocument(
    _id="reg-k240001",
    metadata_content=RegulatoryMetadataContent(
        document_type=DocumentType.REGULATORY_DOC,
        content_type=ContentType.SUMMARY_510K,
        title="AI-Chest Scanner 510(k) Summary",
        k_number="K240001",
        clearance_date=date(2024, 8, 15),
        applicant="Medical AI Corp",
        device_name="AI-Chest Scanner",
        device_class="II",
        product_code="MYN",
        clinical_domain="radiology",
    ),
)

# Add predicate device information
reg_doc.content.predicate_device = PredicateDeviceInfo(
    k_number="K190123",
    device_name="ChestView AI",
    manufacturer="Competitor Inc",
    comparison_summary="Similar intended use for chest x-ray analysis",
)
```

## Use Case Taxonomy

```python
from ashmatics_datamodels.use_cases import (
    UseCaseCategoryBase,
    ClinicalDomain,
)

# Create a use case category
category = UseCaseCategoryBase(
    name="Chest X-ray Analysis",
    description="AI-powered analysis of chest radiographs",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=None,  # Top-level category
    is_active=True,
)

print(category.name)  # "Chest X-ray Analysis"
print(category.clinical_domain)  # ClinicalDomain.RADIOLOGY
```

## Validation

All models include automatic validation:

```python
from ashmatics_datamodels.fda import FDA_510kClearance
from pydantic import ValidationError

try:
    # Invalid K number format
    clearance = FDA_510kClearance(
        k_number="INVALID",  # Should be K######
        device_name="Test Device",
        clearance_date="2024-01-15",
    )
except ValidationError as e:
    print(e)
    # ValidationError: Invalid 510(k) number format...
```

## Working with Validators

```python
from ashmatics_datamodels.common.validators import (
    validate_k_number_format,
    validate_product_code,
    validate_iso_date,
)

# Validate K numbers
k_num = validate_k_number_format("k240001")  # Returns "K240001" (normalized)

# Validate product codes
code = validate_product_code("myn")  # Returns "MYN" (normalized)

# Validate dates
from datetime import date
d = validate_iso_date("2024-08-15")  # Returns date(2024, 8, 15)
```

## Export to JSON

```python
# Export with MongoDB-compatible field names
json_with_aliases = doc.model_dump(by_alias=True)
# Uses "_id" instead of "id"

# Export with Python field names
json_standard = doc.model_dump()
# Uses "id" instead of "_id"

# Export to JSON string
import json
json_string = json.dumps(doc.model_dump(by_alias=True), default=str)
```

## Next Steps

- Explore the [Basic Concepts](concepts.md) to understand the architecture
- Check out detailed [Examples](../examples/fda-clearances.md)
- Browse the [Module Reference](../modules/overview.md)
- Review the [API Reference](../api/common.md) for complete details
