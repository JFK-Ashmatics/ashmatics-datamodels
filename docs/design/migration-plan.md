# Migration Plan

Overview of the phased migration plan for consolidating schemas into ashmatics-core-datamodels.

## Phases

### Phase 1: Core FDA & Regulators ✅ COMPLETE

**Status:** v0.1.0 - Completed 2025-11-21

**Scope:**
- FDA manufacturers, clearances, classifications
- Product and regulatory status schemas
- Use case categories and base schemas
- Common validators and enums
- Multi-jurisdiction regulators and frameworks
- FDA recalls and adverse events

**Deliverables:**
- ✅ `common/` module complete
- ✅ `fda/` module complete
- ✅ `use_cases/` base schemas complete
- ✅ Tests passing
- ✅ Version 0.1.0 released

### Phase 2: MongoDB Documents 🚧 IN PROGRESS

**Status:** v0.2.0 - Active development

**Scope:**
- Three-tier document base classes
- Evidence/publication documents
- Regulatory document schemas
- AI model cards
- Product cards
- Manufacturer cards
- Use case documents

**Deliverables:**
- ✅ `documents/base.py` complete
- ✅ `documents/evidence.py` complete
- ✅ `documents/regulatory.py` complete
- ✅ `documents/models.py` complete
- ✅ `documents/products.py` complete
- ✅ `documents/manufacturers.py` complete
- ✅ `documents/use_cases.py` complete
- 🚧 Tests in progress
- 🚧 Documentation updates

### Phase 3: Ontology Consolidation 📋 PLANNED

**Target:** v0.3.0

**Scope:**
- Consolidate `TermBase`, `TermResponse` from ashmatics-tools
- Migrate value sets and categories
- Consolidate tag schemas
- Add relationship schemas
- Cross-ontology mapping utilities

**Deliverables:**
- `ontology/terms.py`
- `ontology/valuesets.py`
- `ontology/categories.py`
- `ontology/tags.py`
- `ontology/relationships.py`

**Dependencies:**
- Update ashmatics-tools to import from datamodels
- Update KB to import from datamodels
- Resolve duplicate schemas

### Phase 4: Evidence & Quality Metrics 📋 PLANNED

**Target:** v0.4.0

**Scope:**
- Evidence quality schemas
- Evidence provenance tracking
- Evidence timeline schemas
- Author schemas
- Publication metrics

**Deliverables:**
- `evidence/quality.py`
- `evidence/provenance.py`
- `evidence/timeline.py`
- `evidence/authors.py`

### Phase 5: Multi-Jurisdiction 📋 FUTURE

**Target:** v0.5.0+

**Scope:**
- European Medicines Agency (EMA) schemas
- CE Mark and MDR/IVDR schemas
- PMDA (Japan) schemas
- Cross-jurisdiction mapping utilities

**Deliverables:**
- `ema/` module
- `pmda/` module
- Jurisdiction mapping utilities

## Migration Strategy

### For Application Developers

1. **Install datamodels library:**
   ```bash
   uv pip install git+https://github.com/AsherInformatics/ashmatics-core-datamodels.git
   ```

2. **Update imports gradually:**
   ```python
   # Old (KB local schema)
   from app.schemas.clearance_schema import FDA_510kClearance

   # New (from datamodels)
   from ashmatics_datamodels.fda import FDA_510kClearance
   ```

3. **Test thoroughly:**
   - Run existing tests
   - Verify API compatibility
   - Check database serialization

### For Tool Developers

Pipeline pattern for ingestion tools:

```python
# ashmatics-knowledgebase-tools example
from ashmatics_datamodels.fda import FDA_510kClearance
from ashmatics_datamodels.documents import RegulatoryDocument

def process_510k_pdf(pdf_path: str) -> RegulatoryDocument:
    """Parse PDF and create validated document."""
    # 1. Parse with DocLing
    parsed = docling.parse(pdf_path)

    # 2. Validate with datamodels
    clearance = FDA_510kClearance(
        k_number=parsed["k_number"],
        device_name=parsed["device_name"],
        # ... validated locally before API call
    )

    # 3. Create document
    doc = RegulatoryDocument(
        metadata_content=RegulatoryMetadataContent(
            k_number=clearance.k_number,
            device_name=clearance.device_name,
            # ...
        )
    )

    return doc
```

## Version Compatibility

| Version | Python | Pydantic | Breaking Changes |
|---------|--------|----------|------------------|
| 0.1.0   | ≥3.11  | 2.x      | Initial release |
| 0.2.0   | ≥3.11  | 2.x      | Added documents module |
| 0.3.0   | ≥3.11  | 2.x      | TBD (ontology) |

## Related Documents

- [Complete Design Plan](https://github.com/AsherInformatics/ashmatics-core-datamodels/blob/main/docs/Plans/ENGR-DesignPlan-CompleteDataModels-2025-11-21.md)
- [Three-Tier Schema Design](three-tier-schema.md)
