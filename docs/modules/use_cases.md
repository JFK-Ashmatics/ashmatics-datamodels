# use_cases/ Module

The `use_cases/` module provides schemas for organizing clinical AI applications by use case taxonomy.

## Overview

The use case taxonomy helps categorize AI medical devices by:

- Clinical domain (radiology, pathology, cardiology, etc.)
- Clinical specialty (emergency medicine, surgery, etc.)
- Anatomical region (chest, brain, abdomen, etc.)
- Pathology focus (pneumonia, fractures, tumors, etc.)

## Use Case Categories

Hierarchical categorization of clinical AI use cases.

### UseCaseCategoryBase

```python
from ashmatics_datamodels.use_cases import (
    UseCaseCategoryBase,
    ClinicalDomain,
)

category = UseCaseCategoryBase(
    name="Chest X-ray Analysis",
    description="AI-powered analysis of chest radiographs",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=None,  # Top-level category
    is_active=True,
)
```

### Hierarchical Categories

Create nested category trees:

```python
# Parent category
radiology = UseCaseCategoryBase(
    name="Radiology AI",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=None,
)

# Child category
chest_xray = UseCaseCategoryBase(
    name="Chest X-ray",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=radiology.id,  # Links to parent
)

# Grandchild category
pneumonia = UseCaseCategoryBase(
    name="Pneumonia Detection",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=chest_xray.id,
)
```

## Use Cases

Detailed use case definitions with evidence links.

### UseCaseBase

```python
from ashmatics_datamodels.use_cases import (
    UseCaseBase,
    ClinicalDomain,
    ClinicalSpecialty,
    ApplicableProduct,
    SupportingEvidence,
)

use_case = UseCaseBase(
    name="Emergency Department Pneumonia Triage",
    description="AI-assisted triage of chest X-rays for pneumonia in ED",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    clinical_specialty=ClinicalSpecialty.EMERGENCY_MEDICINE,
    category_id="cat-chest-xray",

    # Link applicable products
    applicable_products=[
        ApplicableProduct(
            product_id="prod-001",
            product_name="AI-Chest Scanner",
            k_number="K240001",
        )
    ],

    # Link supporting evidence
    supporting_evidence=[
        SupportingEvidence(
            evidence_id="evidence-001",
            title="Deep Learning for Pneumonia Detection",
            evidence_type="peer_reviewed_paper",
        )
    ],
)
```

## Enums

### ClinicalDomain

Primary clinical domains.

```python
from ashmatics_datamodels.use_cases.enums import ClinicalDomain

# Values:
# RADIOLOGY, PATHOLOGY, CARDIOLOGY, DERMATOLOGY,
# OPHTHALMOLOGY, ONCOLOGY, NEUROLOGY, GASTROENTEROLOGY,
# PULMONOLOGY, ORTHOPEDICS, OTHER
```

### ClinicalSpecialty

Medical specialties.

```python
from ashmatics_datamodels.use_cases.enums import ClinicalSpecialty

# Values:
# EMERGENCY_MEDICINE, SURGERY, INTERNAL_MEDICINE,
# PEDIATRICS, OBSTETRICS_GYNECOLOGY, PSYCHIATRY,
# ANESTHESIOLOGY, PRIMARY_CARE, OTHER
```

### DeploymentModel

How the AI is deployed.

```python
from ashmatics_datamodels.use_cases.enums import DeploymentModel

# Values:
# STANDALONE - Independent software
# INTEGRATED - Embedded in medical device
# CLOUD_BASED - Cloud service
# ON_PREMISE - Local installation
# HYBRID - Combination
```

### IntegrationTarget

Integration points for AI software.

```python
from ashmatics_datamodels.use_cases.enums import IntegrationTarget

# Values:
# PACS - Picture Archiving System
# EHR - Electronic Health Record
# LIS - Laboratory Information System
# RIS - Radiology Information System
# STANDALONE - No integration
```

### EvidenceStrength

Strength of supporting evidence.

```python
from ashmatics_datamodels.use_cases.enums import EvidenceStrength

# Values:
# STRONG - Multiple RCTs or meta-analyses
# MODERATE - Observational studies
# WEAK - Case reports or expert opinion
# INSUFFICIENT - Minimal evidence
```

## Complete Examples

### Building a Use Case Taxonomy

```python
from ashmatics_datamodels.use_cases import (
    UseCaseCategoryBase,
    UseCaseBase,
    ClinicalDomain,
    ClinicalSpecialty,
)

# Top-level: Radiology
radiology = UseCaseCategoryBase(
    name="Radiology AI Applications",
    description="AI applications in diagnostic radiology",
    clinical_domain=ClinicalDomain.RADIOLOGY,
)

# Second-level: Chest Imaging
chest = UseCaseCategoryBase(
    name="Chest Imaging",
    description="Chest X-ray and CT analysis",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=radiology.id,
)

# Third-level: Pneumonia Detection
pneumonia_category = UseCaseCategoryBase(
    name="Pneumonia Detection",
    description="AI-powered pneumonia identification",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=chest.id,
)

# Specific use case
ed_pneumonia = UseCaseBase(
    name="ED Pneumonia Triage",
    description="Emergency department pneumonia screening",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    clinical_specialty=ClinicalSpecialty.EMERGENCY_MEDICINE,
    category_id=pneumonia_category.id,
)
```

### Linking Products to Use Cases

```python
from ashmatics_datamodels.use_cases import (
    UseCaseBase,
    ApplicableProduct,
)

use_case = UseCaseBase(
    name="Diabetic Retinopathy Screening",
    clinical_domain=ClinicalDomain.OPHTHALMOLOGY,
    applicable_products=[
        ApplicableProduct(
            product_id="prod-retina-001",
            product_name="RetinaCheck AI",
            k_number="K230456",
            relevance_score=0.95,
        ),
        ApplicableProduct(
            product_id="prod-retina-002",
            product_name="EyeScan Pro",
            k_number="K230789",
            relevance_score=0.88,
        ),
    ],
)
```

### Linking Evidence to Use Cases

```python
from ashmatics_datamodels.use_cases import (
    UseCaseBase,
    SupportingEvidence,
    EvidenceStrength,
)

use_case = UseCaseBase(
    name="Lung Nodule Detection",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    supporting_evidence=[
        SupportingEvidence(
            evidence_id="pmid-12345678",
            title="Deep Learning for Lung Nodule Detection: A Meta-Analysis",
            evidence_type="meta_analysis",
            strength=EvidenceStrength.STRONG,
            summary="Meta-analysis of 15 RCTs showing 95% sensitivity",
        ),
        SupportingEvidence(
            evidence_id="pmid-87654321",
            title="Real-world Performance of AI Lung Detection",
            evidence_type="observational_study",
            strength=EvidenceStrength.MODERATE,
        ),
    ],
)
```

## File Reference

| File | Purpose |
|------|---------|
| `categories.py` | Use case category schemas |
| `use_cases.py` | Use case definition schemas |
| `enums.py` | Clinical domain and specialty enums |

## Complete API Reference

For detailed API documentation, see [API Reference: use_cases](../api/use_cases.md).
