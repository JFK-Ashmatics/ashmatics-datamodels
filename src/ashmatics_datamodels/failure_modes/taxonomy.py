# Copyright 2026 Asher Informatics PBC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
CHAR failure mode taxonomy document contract: the full shape of the
aigov-framework ``failure_mode_taxonomy.yaml``, so the file round-trips
parse -> validate -> serialize without loss.

Authored per aigov-framework ADR-018 D3. The taxonomy is REFERENCE CONTENT an
assessor works through, resolved at SOP junctions the way the method registry
is (ADR-011) — not a base practice, not a work product, and not another method
name. ``rm-wizard-config.yaml`` RM-2-Q5 keeps offering FMEA, FTA, HAZOP, PHA and
STAMP/STPA as methods; this is what the chosen method is applied to.

ADR-002 binding convention: ``x_ontology_class`` on ``model_config``,
``x_ontology_scheme`` on enum-backed fields. The CI guard is
``tests/failure_modes/test_ontology_binding.py``.

Cross-references needing OTHER files (junction anchors against the aigov-framework
junction inventory, ``{{system.*}}`` condition tokens against the CLF registered
attributes) stay in the aigov-framework validator; this contract owns everything
checkable from the document alone.
"""

from datetime import date

from pydantic import ConfigDict, Field, model_validator

from ashmatics_datamodels.common.base import AshMaticsBaseModel
from ashmatics_datamodels.methods.enums import AIParadigm, OutputForm
from ashmatics_datamodels.methods.methods import EvidenceRef, JunctionRef

from .enums import ActionAuthority, AIFailureMode, RepercussionAudience


class FailureModeApplicability(AshMaticsBaseModel):
    """
    Which systems a failure class is credible for, expressed exclusively as ash
    facet-scheme concepts (zero free strings, ADR-011's success criterion
    carried over).

    An empty axis means "not restricted on this axis", which is the common case
    here and the difference from method applicability: most failure classes are
    reachable by most systems, and the axes exist to exclude the ones that are
    not. Confabulation has no meaning for a system emitting a category.
    """

    ai_paradigm: list[AIParadigm] | None = Field(
        None,
        description="AI paradigms the failure class is credible for; "
        "None means unrestricted.",
        json_schema_extra={"x_ontology_scheme": "ash:AIParadigmScheme"},
    )
    output_form: list[OutputForm] | None = Field(
        None,
        description="Output forms the failure class is credible for; "
        "None means unrestricted.",
        json_schema_extra={"x_ontology_scheme": "ash:OutputFormScheme"},
    )
    action_authority: list[ActionAuthority] | None = Field(
        None,
        description="Action authorities at which the failure class is "
        "credible; None means unrestricted.",
        json_schema_extra={"x_ontology_scheme": "ash:ActionAuthorityScheme"},
    )
    requires_observed_outcome: bool | None = Field(
        None,
        description="True where detectability depends on the outcome ever "
        "being observed and compared against what the system said.",
    )


class Repercussion(AshMaticsBaseModel):
    """
    One half of what makes a failure class usable beside a hazard analysis:
    not what the system did, but what somebody experiences as a result.

    Authored per audience because the audiences diverge. A failure an operator
    sees immediately and an affected person never experiences is a different
    governance problem from one an affected person experiences and no operator
    ever sees.
    """

    audience: RepercussionAudience = Field(
        ..., description="Who experiences this."
    )
    clinical: str | None = Field(
        None, min_length=1,
        description="What is experienced where the system bears on care.",
    )
    non_clinical: str | None = Field(
        None, min_length=1,
        description="What is experienced where it does not — an administrative "
        "system fails differently and the repercussion is not patient harm.",
    )

    @model_validator(mode="after")
    def _at_least_one_framing(self) -> "Repercussion":
        if self.clinical is None and self.non_clinical is None:
            raise ValueError(
                "a repercussion must carry a clinical or a non-clinical "
                "framing; an audience with neither says nothing"
            )
        return self


class FailureModeDefinition(AshMaticsBaseModel):
    """
    One failure class: how a system stops performing as intended, what follows
    from that, and where in CHAR it is consulted. Anchored 1:1 to an
    ``ash:AIFailureModeScheme`` concept whose local name equals ``failure_mode``.
    """

    model_config = ConfigDict(
        json_schema_extra={"x_ontology_class": "ash:AIFailureModeScheme"}
    )

    failure_mode: AIFailureMode = Field(
        ...,
        description="Registry ID and ontology concept local name, fm-* form.",
        json_schema_extra={"x_ontology_scheme": "ash:AIFailureModeScheme"},
    )
    label: str = Field(
        ..., min_length=1,
        description="Human-readable name (the concept's skos:prefLabel).",
    )
    description: str = Field(
        ..., min_length=1,
        description="How the system fails (the concept's skos:definition).",
    )
    what_it_looks_like: list[str] = Field(
        ..., min_length=1,
        description="Concrete presentations an assessor can recognize. The "
        "difference between a taxonomy and a word list.",
    )
    repercussions: list[Repercussion] = Field(
        ..., min_length=1,
        description="What follows from the failure, per audience.",
    )
    applicability: FailureModeApplicability = Field(
        default_factory=FailureModeApplicability,
        description="Which systems this class is credible for.",
    )
    junction_refs: list[JunctionRef] = Field(
        ..., min_length=1,
        description="SOP-step junction anchors (SOP-XX-NN.Sn) where this "
        "taxonomy is consulted, from the authoritative junction inventory.",
    )
    detectable_by: list[str] = Field(
        default_factory=list,
        description="mth:// method IDs, or ASHC control IDs, that would "
        "surface this class. Empty where nothing in CHAR currently would — "
        "which is itself a finding worth leaving visible.",
    )
    evidence_basis: list[EvidenceRef] = Field(
        default_factory=list,
        description="Literature or standards establishing the class. Not "
        "mandatory as it is for methods: several classes here are matters of "
        "system design rather than empirical findings.",
    )
    review: date | None = Field(
        None, description="Date of the last content review of this entry."
    )

    @model_validator(mode="after")
    def _label_is_not_the_id(self) -> "FailureModeDefinition":
        # use_enum_values=True on the repo base model means enum-typed fields
        # hold plain strings after validation; do not reach for .value.
        if self.label.strip().lower() == str(self.failure_mode):
            raise ValueError(
                "label must be a human-readable name, not a repeat of the id"
            )
        return self


class TaxonomyMetadata(AshMaticsBaseModel):
    """The taxonomy_metadata header block."""

    taxonomy_id: str = Field(..., min_length=1)
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    status: str = Field(..., min_length=1)
    scope: str = Field(..., min_length=1)
    created: date
    last_updated: date
    review_cycle: str = Field(..., min_length=1)
    adr_refs: list[str] = Field(default_factory=list)
    jira: str | None = None
    token: str | None = Field(
        None,
        pattern=r"^\{\{[A-Za-z][A-Za-z0-9_]*\}\}$",
        description="The junction token an SOP step renders to show the "
        "org-approved failure classes, as MethodSet.token does for a method "
        "set. One token for the whole taxonomy: an SOP step asks 'which "
        "classes apply here', and the answer is conditioned per system rather "
        "than per junction.",
    )


class FailureModeTaxonomy(AshMaticsBaseModel):
    """The whole ``failure_mode_taxonomy.yaml`` document."""

    taxonomy_metadata: TaxonomyMetadata
    failure_modes: list[FailureModeDefinition] = Field(..., min_length=1)

    @model_validator(mode="after")
    def _ids_unique(self) -> "FailureModeTaxonomy":
        seen: set[str] = set()
        for fm in self.failure_modes:
            fm_id = str(fm.failure_mode)
            if fm_id in seen:
                raise ValueError(f"duplicate failure_mode {fm_id}")
            seen.add(fm_id)
        return self
