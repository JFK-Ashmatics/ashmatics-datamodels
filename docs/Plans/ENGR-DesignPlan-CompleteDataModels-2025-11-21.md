# Engineering Design Plan: Complete AshMatics Core DataModels Library

**Document Type:** Engineering Design Plan
**Created:** 2025-11-21
**Author:** Claude AI Assistant with JF Kalafut
**Status:** Active Planning

---

## Executive Summary

This document inventories all Pydantic schemas and data models across the AshMatics ecosystem that should be consolidated into the `ashmatics-core-datamodels` library. The goal is a single source of truth for data contracts used by:
- **Ashmatics Knowledge Base** (KB)
- **ashmatics-knowledgebase-tools** (ingestion/processing)
- **ashmatics-tools** (SDK with parsers, embedders, ontology)
- **ashmatics-coreapp** (future)

---

## Current State (v0.1.0) - Phase 1 Complete

### common/ Module
| File | Classes | Source |
|------|---------|--------|
| `base.py` | `AshMaticsBaseModel`, `TimestampedModel`, `AuditedModel` | New |
| `enums.py` | `AuthorizationStatus`, `RegulatoryStatus`, `RiskCategory`, `ParsingStatus`, `Region` | KB `enums.py` |
| `validators.py` | `validate_country_code`, `validate_iso_date` | New |
| `regulators.py` | `RegulatorBase`, `RegulatorCreate`, `RegulatorUpdate`, `RegulatorResponse`, `RegulatorSummary`, `RegulatorStats` | KB `regulator_schema.py` |
| `frameworks.py` | `RegulatoryFrameworkBase`, `RegulatoryFrameworkCreate`, `RegulatoryFrameworkUpdate`, `RegulatoryFrameworkResponse`, `RegulatoryFrameworkSummary`, `RegulatoryFrameworkStats` | KB `regulatory_framework_schema.py` |

### fda/ Module
| File | Classes | Source |
|------|---------|--------|
| `enums.py` | `ClearanceType`, `FDA_DeviceClass`, `Modality`, `SubmissionType`, `ReviewPanel` | KB `enums.py` |
| `manufacturers.py` | `FDA_ManufacturerBase`, `FDA_ManufacturerCreate`, `FDA_ManufacturerResponse`, `FDA_ManufacturerAddress` | KB + Plan |
| `clearances.py` | `FDA_ClearanceBase`, `FDA_510kClearance*`, `FDA_PMAClearance`, `FDA_DeNovoClearance`, `FDA_PredicateDevice`, `RegulatoryAuthorization*` | KB `clearance_schema.py`, `regulatory_authorization_schema.py` |
| `classifications.py` | `FDA_ProductCode`, `FDA_DeviceClassification`, `ProductClassificationBase/Create/Response`, `ProductClassificationSystemBase/Create/Response`, `ClassificationSystemInfo` | KB `product_classification_schema.py`, `product_classification_system_schema.py` |
| `products.py` | `FDA_ProductBase/Create/Response`, `ProductRegulatoryStatusBase/Create/Update/Response/Stats` | KB `product_regulatory_status_schema.py` |
| `recalls.py` | `FDA_RecallBase/Create/Response/Stats`, `RecallStatus`, `RecallClass`, `RecallType` | New (OpenFDA aligned) |
| `adverse_events.py` | `FDA_AdverseEventBase/Create/Response/Stats`, `FDA_MAUDEDevice`, `FDA_MAUDEPatient`, `EventType`, `ReportSourceCode`, `DeviceOperator` | New (OpenFDA aligned) |

### use_cases/ Module
| File | Classes | Source |
|------|---------|--------|
| `enums.py` | `ClinicalDomain`, `ClinicalSpecialty`, `DeploymentModel`, `IntegrationTarget`, `EvidenceStrength` | New |
| `categories.py` | `UseCaseCategoryBase`, `UseCaseCategoryCreate`, `UseCaseCategoryResponse`, `UseCaseCategoryTree` | KB `use_case_category_schema.py` |
| `use_cases.py` | `UseCaseBase`, `UseCaseCreate`, `UseCaseResponse`, `ApplicableProduct`, `SupportingEvidence` | New |

---

## Remaining Schemas to Migrate

### Priority 1: Core Regulatory & Product ✅ COMPLETE

All Priority 1 schemas have been migrated. See "Current State" section above for details.

---

### Priority 2: Evidence & Publications

#### From KB `src/app/schemas/`

| Schema File | Classes to Migrate | Target Module |
|-------------|-------------------|---------------|
| `evidence_schema.py` | `EvidenceBase`, `EvidenceCreate`, `EvidencePublic`, `EvidenceWithRelations` | `evidence/publications.py` |
| `evidence_author_schema.py` | `EvidenceAuthorBase`, `EvidenceAuthorResponse` | `evidence/authors.py` |
| `evidence_quality_schema.py` | `EvidenceQualityBase`, `EvidenceQualityMetrics` | `evidence/quality.py` |
| `evidence_provenance_schema.py` | `EvidenceProvenanceBase` | `evidence/provenance.py` |
| `evidence_timeline_schema.py` | `EvidenceTimelineBase` | `evidence/timeline.py` |

---

### Priority 3: Ontology & Terms (Consolidate from ashmatics-tools)

#### From `ashmatics-tools/src/ashmatics_tools/ontology/`

| Source File | Classes to Migrate | Target Module |
|-------------|-------------------|---------------|
| `terms/schemas.py` | `TermBase`, `TermCreate`, `TermResponse`, `TermDB`, `OntologyMapping`, `TermRelationship`, `TermRelationshipType`, `TermValue`, `TermValidationResponse` | `ontology/terms.py` |
| `terms/valueset_schemas.py` | `ValueSetBase`, `ValueSetCreate`, `ValueSetResponse` | `ontology/valuesets.py` |
| `categories/schemas.py` | `CategoryBase`, `CategoryResponse` | `ontology/categories.py` |

#### From KB `src/app/schemas/ontology/`

| Source File | Classes | Notes |
|-------------|---------|-------|
| `term_schema.py` | Duplicate of ashmatics-tools | Consolidate |
| `tags_schema.py` | `TagBase`, `TagResponse`, `TagValueResponse` | `ontology/tags.py` |
| `valueset_schema.py` | `ValueSetBase`, `ValueSetResponse` | Consolidate with tools |
| `category_schema.py` | `CategoryBase`, `CategoryResponse` | Consolidate |
| `relationship_schema.py` | `RelationshipBase`, `RelationshipResponse` | `ontology/relationships.py` |
| `webhooks_schema.py` | `WebhookBase`, `WebhookResponse` | `common/webhooks.py` (generic) |

---

### Priority 4: AI Model Cards & Knowledge Base Cards

#### From KB `src/app/schemas/`

| Schema File | Classes to Migrate | Target Module |
|-------------|-------------------|---------------|
| `knowledge_base_model_card_schema.py` | `KBModelCardBase`, `KBModelCardCreate`, `KBModelCardResponse` | `ai_models/model_cards.py` |
| `knowledge_base_manufacturer_card_schema.py` | `KBManufacturerCardBase`, `KBManufacturerCardResponse` | `manufacturers/cards.py` |
| `ai_model_card_registry_schema.py` | `AIModelCardRegistryBase` | `ai_models/registry.py` |

---

### Priority 5: Documents & Search

#### From KB `src/app/schemas/`

| Schema File | Classes to Migrate | Target Module |
|-------------|-------------------|---------------|
| `document_schema.py` | `DocumentBase`, `DocumentCreate`, `DocumentSummary`, `DocumentDetail`, `SearchQuery` | `documents/base.py` |
| `search_schema.py` | `SearchQueryBase`, `SearchResultBase`, `FacetResponse` | `search/schemas.py` |

---

### Priority 6: Users & System (Application-Specific - May Not Migrate)

| Schema File | Decision | Reason |
|-------------|----------|--------|
| `user_schema.py` | **Keep in KB** | Application-specific auth |
| `manufacturer_developer_link_schema.py` | **Keep in KB** | Junction table, app-specific |

---

## Proposed Final Package Structure

```
ashmatics_datamodels/
├── __init__.py
├── common/
│   ├── __init__.py
│   ├── base.py              # ✅ Done
│   ├── enums.py             # ✅ Done
│   ├── validators.py        # ✅ Done
│   ├── regulators.py        # NEW: Multi-jurisdiction regulators
│   ├── frameworks.py        # NEW: Regulatory frameworks
│   └── webhooks.py          # NEW: Generic webhook schemas
│
├── fda/
│   ├── __init__.py          # ✅ Done
│   ├── enums.py             # ✅ Done
│   ├── manufacturers.py     # ✅ Done
│   ├── clearances.py        # ✅ Done (extend)
│   ├── classifications.py   # ✅ Done (extend)
│   ├── products.py          # NEW: Product schemas
│   ├── recalls.py           # NEW: Recall schemas
│   └── adverse_events.py    # NEW: MAUDE schemas
│
├── ema/                     # Future: European Medicines Agency
│   ├── __init__.py
│   ├── manufacturers.py
│   └── authorizations.py    # CE Mark, MDR/IVDR
│
├── use_cases/
│   ├── __init__.py          # ✅ Done
│   ├── enums.py             # ✅ Done
│   ├── categories.py        # ✅ Done
│   └── use_cases.py         # ✅ Done
│
├── evidence/                # NEW MODULE
│   ├── __init__.py
│   ├── publications.py      # Publications/papers
│   ├── authors.py           # Author schemas
│   ├── quality.py           # Evidence quality metrics
│   ├── provenance.py        # Source tracking
│   └── timeline.py          # Temporal tracking
│
├── ontology/                # NEW MODULE (from ashmatics-tools)
│   ├── __init__.py
│   ├── terms.py             # Term schemas
│   ├── valuesets.py         # Value set schemas
│   ├── categories.py        # Category schemas
│   ├── tags.py              # Tag schemas
│   ├── relationships.py     # Relationship schemas
│   └── mappings.py          # Cross-ontology mappings
│
├── ai_models/               # NEW MODULE
│   ├── __init__.py
│   ├── model_cards.py       # AI model card schemas
│   └── registry.py          # Model registry schemas
│
├── manufacturers/           # NEW MODULE (extend from fda/)
│   ├── __init__.py
│   └── cards.py             # Manufacturer profile cards
│
├── documents/               # NEW MODULE
│   ├── __init__.py
│   ├── base.py              # Base document schemas
│   └── mongodb.py           # MongoDB-specific schemas
│
├── search/                  # NEW MODULE
│   ├── __init__.py
│   └── schemas.py           # Search query/result schemas
│
└── utils/
    ├── __init__.py          # ✅ Done (empty)
    ├── parsing.py           # NEW: Parsing utilities
    └── normalization.py     # NEW: Name/code normalization
```

---

## Duplication Analysis

### Critical Duplications to Resolve

| Schema | KB Location | Tools Location | Resolution |
|--------|-------------|----------------|------------|
| `TermBase`, `TermResponse` | `schemas/ontology/term_schema.py` | `ashmatics-tools/ontology/terms/schemas.py` | **Consolidate in datamodels** |
| `ValueSetBase` | `schemas/ontology/valueset_schema.py` | `ashmatics-tools/ontology/terms/valueset_schemas.py` | **Consolidate in datamodels** |
| `CategoryBase` | `schemas/ontology/category_schema.py` | `ashmatics-tools/ontology/categories/schemas.py` | **Consolidate in datamodels** |
| `TagBase` | `schemas/ontology/tags_schema.py` | `schemas/tags_schema.py` | **Already duplicated in KB! Consolidate** |

---

## Migration Strategy

### Phase 1: 510k Ingestion Support (COMPLETED 2025-11-21)
1. ✅ FDA enums, manufacturers, clearances, classifications
2. ✅ Use case categories and base schemas
3. ✅ Add `fda/products.py` for product schemas
4. ✅ Extend `fda/clearances.py` with regulatory authorization fields
5. ✅ Add `common/regulators.py` for multi-jurisdiction regulator schemas
6. ✅ Add `common/frameworks.py` for regulatory framework schemas
7. ✅ Extend `fda/classifications.py` with ProductClassification and ClassificationSystem

### Phase 2: Ontology Consolidation (Next Sprint)
1. ⬜ Create `ontology/` module
2. ⬜ Migrate `TermBase`, `TermResponse`, `TermDB` from ashmatics-tools
3. ⬜ Migrate valuesets, categories, tags
4. ⬜ Update ashmatics-tools to import from datamodels
5. ⬜ Update KB to import from datamodels

### Phase 3: Evidence & Publications
1. ⬜ Create `evidence/` module
2. ⬜ Migrate evidence schemas from KB
3. ⬜ Add evidence quality and provenance

### Phase 4: AI Models & Documents
1. ⬜ Create `ai_models/` module
2. ⬜ Create `documents/` module
3. ⬜ Migrate model card and document schemas

### Phase 5: Multi-Jurisdiction (Future)
1. ⬜ Create `ema/` module for European schemas
2. ⬜ Create cross-jurisdiction mapping utilities

---

## Dependencies & Consumers

### Applications That Will Import from datamodels

| Application | Current State | Migration Effort | Notes |
|-------------|---------------|------------------|-------|
| **Ashmatics KB** | Local schemas in `src/app/schemas/` | Medium | Gradual replacement of local schemas |
| **ashmatics-tools** | Local schemas in `ontology/terms/schemas.py` | Medium | Ontology consolidation focus |
| **ashmatics-knowledgebase-tools** | No local schemas currently | Medium | **Will need datamodels for DocLing ingestion pipelines** - structured validation before API calls |
| **ashmatics-coreapp** | TBD | Low | Greenfield - can use datamodels from start |

### Ingestion Pipeline Pattern

The `ashmatics-knowledgebase-tools` repo will use datamodels for type-safe document processing:

```python
# Example: ashmatics-knowledgebase-tools/src/fda/importers/fda_documents_importer.py

from ashmatics_datamodels.fda import FDA_510kClearance, FDA_ManufacturerBase, FDA_DeviceClass

def process_parsed_510k(docling_output: dict) -> FDA_510kClearance:
    """
    Transform DocLing-parsed PDF into validated schema before KB API call.

    Benefits:
    - IDE autocomplete for field names
    - Pre-validation catches errors before API round-trip
    - Type safety throughout pipeline
    - Consistent vocabulary (k_number vs clearance_number)
    """
    return FDA_510kClearance(
        k_number=docling_output.get("k_number"),
        device_name=docling_output.get("device_name"),
        device_class=FDA_DeviceClass.CLASS_2,
        manufacturer_name=docling_output.get("manufacturer"),
        decision_date=docling_output.get("decision_date"),
        # ... validated locally, then serialized to JSON for KB API
    )
```

### pyproject.toml Updates Required

**KB:**
```toml
dependencies = [
    "ashmatics-datamodels @ git+https://github.com/AsherInformatics/ashmatics-core-datamodels.git",
]
```

**ashmatics-tools:**
```toml
dependencies = [
    "ashmatics-datamodels @ git+https://github.com/AsherInformatics/ashmatics-core-datamodels.git",
]
```

---

## Versioning Plan

| Version | Scope | Target Date |
|---------|-------|-------------|
| **v0.1.0** | ✅ FDA core, use cases base | 2025-11-21 |
| **v0.2.0** | Ontology module (terms, valuesets, tags) | TBD |
| **v0.3.0** | Evidence module | TBD |
| **v0.4.0** | AI models, documents | TBD |
| **v1.0.0** | Stable API, all migrations complete | TBD |

---

## Open Questions

1. **MongoDB ObjectId handling**: The `ashmatics-tools` `TermDB` class has custom `PyObjectId` handling. Should this be in the datamodels library or remain application-specific?

2. **Validation stringency**: Should validators be strict (raise errors) or lenient (coerce/normalize)? Currently using strict.

3. **Backward compatibility**: When KB/tools import from datamodels, do we need deprecation aliases in the original locations?

---

## Related Documents

- [Original DataModels Library Plan](../../Ashmatics_Knowledgebase/docs/Plans/ENGR-DesignPlan-AshMaticsCoreDataModelsLibrary-2025-11-17.md)
- [MongoDB Document Schema Plan](../../Ashmatics_Knowledgebase/docs/Plans/DocumentDataModelSchema-Normalize-2025-11-15/ENGR-DesignPlan-mongoDocumentModel-2025-11-15.md)
- [OpenFDA Harmonization Plan](../../Ashmatics_Knowledgebase/docs/Plans/TerminologyHarmonization-openFDA-2025-11-17/)

---

## Document Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-21 | 1.0 | Initial inventory and migration plan | Claude AI + JF Kalafut |
