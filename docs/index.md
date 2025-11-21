# AshMatics Core DataModels

Welcome to the **AshMatics Core DataModels** documentation. This library provides canonical Pydantic data models for healthcare regulatory data, clinical AI use cases, and knowledge base documents.

## Overview

AshMatics Core DataModels serves as the **single source of truth** for data contracts across the AshMatics ecosystem:

- **Knowledge Base (KB)** - FastAPI backend
- **ashmatics-tools** - SDK with parsers and ontology
- **ashmatics-knowledgebase-tools** - Document ingestion pipelines
- **AI Watch applications** - Clinical AI surveillance tools

## Key Features

### 🏥 FDA Vocabulary
OpenFDA-aligned schemas for manufacturers, 510(k) clearances, device classifications, recalls, and adverse events (MAUDE).

### 📄 MongoDB Document Schemas
Standardized three-tier structure for all `kb_*` collections:
- **Tier 1**: Artifact metadata (provenance, storage)
- **Tier 2**: Content metadata (search, classification)
- **Tier 3**: Document body (sections, figures, tables)

### 🔬 Use Case Taxonomy
Clinical AI use case categorization with specialty, domain, and anatomical focus.

### ✅ Rich Validation
Built-in validators for regulatory identifiers (K numbers, product codes), dates, and country codes.

### 🔐 Type Safe
Full type hints with mypy support for IDE autocomplete and static analysis.

### 🗄️ Database Agnostic
Pure Pydantic models with no ORM coupling - works with any backend.

## Quick Example

```python
from ashmatics_datamodels.fda import (
    FDA_ManufacturerBase,
    FDA_510kClearance,
    FDA_DeviceClass,
)

# Create a manufacturer
manufacturer = FDA_ManufacturerBase(
    manufacturer_name="Medical AI Corp",
    applicant="Medical AI Corp",
)

# Create a validated 510(k) clearance
clearance = FDA_510kClearance(
    k_number="K240001",  # Auto-validated format
    clearance_date="2024-08-15",
    device_name="AI-Chest Scanner",
    device_class=FDA_DeviceClass.CLASS_2,
    applicant="Medical AI Corp",
)
```

## Architecture

```
ashmatics_datamodels/
├── common/          # Base models, validators, regulators, frameworks
├── fda/             # FDA vocabulary (clearances, recalls, adverse events)
├── documents/       # MongoDB three-tier document schemas
├── use_cases/       # Clinical AI use case taxonomy
└── utils/           # Parsing and normalization utilities
```

## Current Version

**v0.2.0** - Phase 2 in progress

- ✅ Phase 1 Complete: FDA core schemas, use cases, regulators
- 🚧 Phase 2 Active: MongoDB document schemas
- 📋 Phase 3 Planned: Ontology consolidation
- 📋 Phase 4 Planned: Evidence quality metrics

## Getting Started

Ready to dive in? Check out the [Installation Guide](getting-started/installation.md) and [Quick Start](getting-started/quickstart.md).

## License

Apache 2.0 - See [LICENSE](https://github.com/AsherInformatics/ashmatics-core-datamodels/blob/main/LICENSE) for details.

---

**Maintained by:** Asher Informatics PBC
**Contact:** info@asherinformatics.com
