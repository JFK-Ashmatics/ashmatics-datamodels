# Basic Concepts

This page explains the core architectural concepts in AshMatics Core DataModels.

## Design Philosophy

### Pure Pydantic Models
All models are pure Pydantic v2 models with **no ORM coupling**. This means:

- ✅ Works with any database backend (MongoDB, PostgreSQL, SQLite)
- ✅ Easy to serialize/deserialize
- ✅ Full type safety and IDE support
- ✅ Portable across applications
- ❌ No SQLAlchemy or Beanie dependencies
- ❌ No business logic (validation only)

### Strict Validation
Models use strict validation with a **fail-fast** approach:

- Invalid data raises `ValidationError` immediately
- Automatic normalization (uppercase codes, trimmed strings)
- Format checking with regex patterns
- Range validation for numeric fields

### OpenFDA Alignment
FDA schemas mirror [OpenFDA API](https://open.fda.gov/) structures:

- Field names match OpenFDA JSON keys
- Enums align with OpenFDA terminology
- Compatible date formats (ISO 8601 and US formats)

## Base Model Hierarchy

All models inherit from `AshMaticsBaseModel`:

```python
from ashmatics_datamodels.common import AshMaticsBaseModel

class AshMaticsBaseModel(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,      # Serialize enums as values
        validate_assignment=True,   # Validate on field assignment
    )
```

### TimestampedModel
For models requiring automatic timestamp tracking:

```python
from ashmatics_datamodels.common import TimestampedModel

class MyModel(TimestampedModel):
    name: str
    # created_at and updated_at auto-generated
```

### AuditedModel
For models requiring full audit trails:

```python
from ashmatics_datamodels.common import AuditedModel

class MyModel(AuditedModel):
    name: str
    # Includes created_at, updated_at, created_by, updated_by
```

## Three-Tier MongoDB Schema

All `kb_*` MongoDB collections follow a standardized three-tier structure:

```
MongoDocumentBase
├── Tier 1: metadata_object    (Artifact metadata)
├── Tier 2: metadata_content   (Content classification)
└── Tier 3: content            (Document body)
```

### Tier 1: metadata_object
**Purpose:** Track the document as a stored artifact

**Contains:**
- Provenance (created_at, created_by, version)
- Storage (file_size, storage_location, checksum)
- Processing (pipeline, errors, completion time)

**Example:**
```python
MetadataObjectBase(
    created_at=datetime.now(timezone.utc),
    created_by="system",
    version="1.0",
    storage_location="s3://kb-evidence/papers/file.pdf",
    processing_pipeline="grobid_v0.7.2",
)
```

### Tier 2: metadata_content
**Purpose:** Classify and categorize content for search/filtering

**Contains:**
- Document type (evidence, regulatory, model card)
- Content type (peer-reviewed paper, 510k summary)
- Searchable metadata (title, authors, keywords)
- Classification (clinical domain, specialty)

**Example:**
```python
EvidenceMetadataContent(
    document_type=DocumentType.EVIDENCE_DOC,
    content_type=ContentType.PEER_REVIEWED_PAPER,
    title="Deep Learning for Radiology",
    clinical_domain="radiology",
    authors=["Dr. Smith"],
)
```

### Tier 3: content
**Purpose:** Store the actual document body

**Contains:**
- Hierarchical sections (with subsections)
- Figures and tables
- Citations and references
- Type-specific fields

**Example:**
```python
ContentBase(
    sections={
        "1_intro": SectionBase(title="Introduction", order=1, text="..."),
        "2_methods": SectionBase(title="Methods", order=2, text="..."),
    },
    figures=[FigureReference(figure_id="fig1", caption="...")],
    references=[CitationReference(ref_id="ref1", doi="...")],
)
```

## Module Organization

### common/
Cross-jurisdictional base models and utilities

- **base.py** - `AshMaticsBaseModel`, `TimestampedModel`, `AuditedModel`
- **validators.py** - Shared validators (dates, country codes, K numbers)
- **enums.py** - Global enums (`AuthorizationStatus`, `RiskCategory`)
- **regulators.py** - Multi-jurisdiction regulator schemas
- **frameworks.py** - Regulatory framework schemas

### fda/
FDA-specific vocabulary aligned with OpenFDA

- **manufacturers.py** - Manufacturer and contact schemas
- **clearances.py** - 510(k), PMA, De Novo clearances
- **classifications.py** - Product codes and device classifications
- **products.py** - Product and regulatory status
- **recalls.py** - FDA recall information
- **adverse_events.py** - MAUDE adverse event reports

### use_cases/
Clinical AI use case taxonomy

- **categories.py** - Hierarchical use case categories
- **use_cases.py** - Use case definitions with evidence links
- **enums.py** - Clinical domain, specialty, deployment model enums

### documents/
MongoDB three-tier document schemas

- **base.py** - Base classes for all `kb_*` collections
- **evidence.py** - Scientific evidence and publications
- **regulatory.py** - Regulatory documents (510k summaries)
- **models.py** - AI model cards
- **products.py** - Product profile cards
- **manufacturers.py** - Manufacturer profile cards
- **use_cases.py** - Clinical use case documents

## Validation Examples

### K Number Validation
```python
from ashmatics_datamodels.common.validators import validate_k_number_format

# Valid formats
validate_k_number_format("K240001")    # Returns "K240001"
validate_k_number_format("k240001")    # Returns "K240001" (normalized)
validate_k_number_format("BK240001")   # Returns "BK240001" (CBER)
validate_k_number_format("DEN240001")  # Returns "DEN240001" (De Novo)

# Invalid formats
validate_k_number_format("INVALID")    # Raises ValueError
validate_k_number_format("K12345")     # Raises ValueError (too short)
```

### Date Validation
```python
from ashmatics_datamodels.common.validators import validate_iso_date

# ISO 8601 format
validate_iso_date("2024-08-15")  # Returns date(2024, 8, 15)

# US format
validate_iso_date("08/15/2024")  # Returns date(2024, 8, 15)

# Invalid format
validate_iso_date("15-08-2024")  # Raises ValueError
```

### Product Code Validation
```python
from ashmatics_datamodels.common.validators import validate_product_code

# Valid 3-letter codes
validate_product_code("MYN")  # Returns "MYN"
validate_product_code("myn")  # Returns "MYN" (normalized)

# Invalid codes
validate_product_code("MY")    # Raises ValueError (too short)
validate_product_code("MYNA")  # Raises ValueError (too long)
```

## Document Summaries

Each document type has a corresponding summary schema for efficient list views:

```python
from ashmatics_datamodels.documents import EvidenceDocument, EvidenceSummary

# Full document with all tiers
full_doc = EvidenceDocument(...)

# Create lightweight summary (no content)
summary = EvidenceSummary.from_document(full_doc)

# Summary contains only:
# - id, title, authors, journal
# - clinical_domain, tags
# - created_at, updated_at
```

Summaries are useful for:
- Search result listings
- Pagination
- API responses that don't need full content
- Reducing payload size

## JSON Serialization

### With MongoDB Aliases
```python
# Uses "_id" for MongoDB compatibility
json_data = doc.model_dump(by_alias=True)
# {"_id": "123", "metadata_object": {...}, ...}
```

### With Python Field Names
```python
# Uses "id" for Python objects
json_data = doc.model_dump()
# {"id": "123", "metadata_object": {...}, ...}
```

### Handle Dates
```python
import json

# Use default=str to serialize dates/datetimes
json_string = json.dumps(doc.model_dump(), default=str)
```

## Next Steps

- See [Examples](../examples/fda-clearances.md) for detailed usage patterns
- Explore the [Module Reference](../modules/overview.md) for each module
- Review the [API Reference](../api/common.md) for complete API details
