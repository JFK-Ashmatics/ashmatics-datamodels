# Use Case Taxonomy Examples

Examples for working with clinical AI use case schemas.

## Creating Use Case Categories

```python
from ashmatics_datamodels.use_cases import (
    UseCaseCategoryBase,
    ClinicalDomain,
)

# Top-level category
radiology = UseCaseCategoryBase(
    name="Radiology AI Applications",
    description="AI applications in diagnostic radiology",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=None,
    is_active=True,
)

# Child category
chest_imaging = UseCaseCategoryBase(
    name="Chest Imaging",
    description="Chest X-ray and CT analysis",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=radiology.id,
    is_active=True,
)

# Grandchild category
pneumonia = UseCaseCategoryBase(
    name="Pneumonia Detection",
    description="AI-powered pneumonia identification",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    parent_category_id=chest_imaging.id,
    is_active=True,
)
```

## Creating Use Cases

```python
from ashmatics_datamodels.use_cases import (
    UseCaseBase,
    ClinicalDomain,
    ClinicalSpecialty,
)

use_case = UseCaseBase(
    name="Emergency Department Pneumonia Triage",
    description="AI-assisted triage of chest X-rays for pneumonia in the emergency department",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    clinical_specialty=ClinicalSpecialty.EMERGENCY_MEDICINE,
    category_id="cat-pneumonia-001",
)
```

## Linking Products to Use Cases

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

## Linking Evidence to Use Cases

```python
from ashmatics_datamodels.use_cases import (
    UseCaseBase,
    SupportingEvidence,
    EvidenceStrength,
)

use_case = UseCaseBase(
    name="Lung Nodule Detection in CT",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    supporting_evidence=[
        SupportingEvidence(
            evidence_id="pmid-12345678",
            title="Deep Learning for Lung Nodule Detection: A Meta-Analysis",
            evidence_type="meta_analysis",
            strength=EvidenceStrength.STRONG,
            summary="Meta-analysis of 15 RCTs showing 95% sensitivity and 93% specificity",
        ),
        SupportingEvidence(
            evidence_id="pmid-87654321",
            title="Real-world Performance of AI Lung Detection in 10 Hospitals",
            evidence_type="observational_study",
            strength=EvidenceStrength.MODERATE,
            summary="Observational study with 10,000 patients",
        ),
    ],
)
```

## Complete Taxonomy Example

```python
from ashmatics_datamodels.use_cases import (
    UseCaseCategoryBase,
    UseCaseBase,
    ClinicalDomain,
    ClinicalSpecialty,
    ApplicableProduct,
    SupportingEvidence,
    EvidenceStrength,
)

# Build taxonomy
categories = {
    "radiology": UseCaseCategoryBase(
        name="Radiology",
        clinical_domain=ClinicalDomain.RADIOLOGY,
    ),
    "chest": UseCaseCategoryBase(
        name="Chest Imaging",
        clinical_domain=ClinicalDomain.RADIOLOGY,
        parent_category_id="radiology",
    ),
    "pneumonia": UseCaseCategoryBase(
        name="Pneumonia Detection",
        clinical_domain=ClinicalDomain.RADIOLOGY,
        parent_category_id="chest",
    ),
}

# Create use case
ed_pneumonia = UseCaseBase(
    name="ED Pneumonia Triage",
    description="AI triage in emergency department",
    clinical_domain=ClinicalDomain.RADIOLOGY,
    clinical_specialty=ClinicalSpecialty.EMERGENCY_MEDICINE,
    category_id="pneumonia",
    applicable_products=[
        ApplicableProduct(
            product_id="prod-001",
            product_name="ChestAI Scanner",
            k_number="K240001",
        )
    ],
    supporting_evidence=[
        SupportingEvidence(
            evidence_id="evidence-001",
            title="AI for ED Pneumonia Detection",
            evidence_type="randomized_controlled_trial",
            strength=EvidenceStrength.STRONG,
        )
    ],
)
```
