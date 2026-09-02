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
Platform mechanism-availability record, and the three-gate assurance ceiling.

The ontology's ``ashcai:MechanismAvailabilityScheme`` defines the vocabulary
and says where assignments do NOT live: not in the ontology, not in the
governance catalog, because they move on the product release cadence. The
assignments live in **asher-infra** (``platform-capabilities/
mechanism-availability.yaml``), pinned by each release manifest alongside
the repo tags; this module is the contract that file, coreapp and the
aigov-framework validator all validate against.

The record is per mechanism FAMILY and per EDITION. Edition belongs here
because Essentials and Enterprise genuinely differ in what the platform can
execute (an on-tenant collector exists for one and not the other), and that
is a fact about the platform, not about a customer's tier or a build's
rollout phase.

An Essentials value may further be split by the SOURCE SYSTEM's deployment
mode (``ash:DeploymentModeScheme``). Essentials is hosted only, so its
reach to a source is structural: a cloud-hosted AI vendor is reachable, an
on-premise PACS is not, whatever the customer would like. Enterprise is a
single value because a customer-side deployment reaches everything.

Three gates compose to a control's achievable assurance ceiling::

    declared    framework  ->  this evidence item can come from mechanism M
    available   platform   ->  M is none | planned | beta | GA | partner
    entitled    customer   ->  this site may AND can actually use M — licence,
                               module, and whether its IT will open the path;
                               a 100-hour security review is this gate, not
                               availability and not the customer's governance

    achievable_ceiling = strongest yieldsAssuranceMode across declared
                         mechanisms that are both available and entitled

The gap between a profile's ``assurance.target`` and the ceiling is
diagnostic and resolves to three different meetings (``GapCause``): caused
by availability it is a product backlog item; by entitlement a licensing
conversation; by neither the customer's own governance work.
"""

import re
from collections.abc import Callable, Iterable
from datetime import date
from enum import Enum

from pydantic import ConfigDict, Field, model_validator

from ashmatics_datamodels.common.base import AshMaticsBaseModel

from .enums import (
    ASSURANCE_ORDINAL,
    AVAILABILITY_ORDINAL,
    YIELDS_ASSURANCE_MODE,
    AssuranceMode,
    DeploymentMode,
    Edition,
    EvidenceMechanism,
    MechanismAvailability,
)

# Component tokens are the release manifest's ``repos:`` keys (or a partner
# name), so "who provides this" joins to "what version shipped" for free.
COMPONENT_TOKEN_PATTERN = r"^[a-z][a-z0-9-]*[a-z0-9]$"

# Below this state a mechanism does not count toward the ceiling. ``beta`` is
# usable with a named site under limited support; the scheme says evidence it
# produces should be corroborated before an accreditation claim rests on it,
# which is a claim about how to read the evidence, not whether it exists.
DEFAULT_MINIMUM_AVAILABILITY = MechanismAvailability.BETA


class ByDeploymentMode(AshMaticsBaseModel):
    """Availability split by the source system's deployment mode. All four
    modes are required, for the same reason both editions are."""

    cloud: MechanismAvailability = Field(
        ..., json_schema_extra={"x_ontology_scheme": "ashcai:MechanismAvailabilityScheme"}
    )
    on_premise: MechanismAvailability = Field(
        ..., json_schema_extra={"x_ontology_scheme": "ashcai:MechanismAvailabilityScheme"}
    )
    hybrid: MechanismAvailability = Field(
        ..., json_schema_extra={"x_ontology_scheme": "ashcai:MechanismAvailabilityScheme"}
    )
    edge: MechanismAvailability = Field(
        ..., json_schema_extra={"x_ontology_scheme": "ashcai:MechanismAvailabilityScheme"}
    )

    def for_mode(self, mode: DeploymentMode | str | None) -> MechanismAvailability:
        """The value for one mode; with no mode known, the WEAKEST across
        modes, so an unqualified reading never overstates reach."""
        if mode is None:
            return min(
                (MechanismAvailability(getattr(self, m.value)) for m in DeploymentMode),
                key=lambda a: AVAILABILITY_ORDINAL[a],
            )
        return MechanismAvailability(getattr(self, DeploymentMode(mode).value))


class EditionAvailability(AshMaticsBaseModel):
    """Availability of one mechanism family, stated per edition. Both
    editions are required: an unstated edition is indistinguishable from
    ``none`` to a reader and from ``generally_available`` to a bug.

    Essentials may be a single value or a ``ByDeploymentMode`` split.
    Enterprise is always a single value."""

    essentials: MechanismAvailability | ByDeploymentMode = Field(
        ...,
        description="Availability on the Essentials edition (Asher-hosted only, "
        "self-serve), optionally split by the source system's deployment mode.",
        json_schema_extra={"x_ontology_scheme": "ashcai:MechanismAvailabilityScheme"},
    )
    enterprise: MechanismAvailability = Field(
        ...,
        description="Availability on the Enterprise edition (Asher-hosted or "
        "customer tenant).",
        json_schema_extra={"x_ontology_scheme": "ashcai:MechanismAvailabilityScheme"},
    )

    def for_edition(
        self, edition: Edition | str, deployment_mode: DeploymentMode | str | None = None
    ) -> MechanismAvailability:
        v = getattr(self, Edition(edition).value)
        if isinstance(v, ByDeploymentMode):
            return v.for_mode(deployment_mode)
        return MechanismAvailability(v)

    def strongest(self) -> MechanismAvailability:
        """Best value anywhere in the entry — what `provided_by` must back."""
        vals = [MechanismAvailability(self.enterprise)]
        e = self.essentials
        vals += (
            [MechanismAvailability(getattr(e, m.value)) for m in DeploymentMode]
            if isinstance(e, ByDeploymentMode) else [MechanismAvailability(e)]
        )
        return max(vals, key=lambda a: AVAILABILITY_ORDINAL[a])


class MechanismAvailabilityEntry(AshMaticsBaseModel):
    """One mechanism family's platform availability."""

    model_config = ConfigDict(
        json_schema_extra={"x_ontology_class": "ashcai:EvidenceMechanismScheme"},
    )

    mechanism: EvidenceMechanism = Field(
        ...,
        description="Evidence mechanism family (skos:notation).",
        json_schema_extra={"x_ontology_scheme": "ashcai:EvidenceMechanismScheme"},
    )
    availability: EditionAvailability
    provided_by: list[str] = Field(
        default_factory=list,
        description="Components that execute this mechanism — release manifest "
        "`repos:` keys (e.g. ashmatics-coreapp) or a partner name. Empty when "
        "availability is none or planned.",
    )
    depends_on_any: list[EvidenceMechanism] = Field(
        default_factory=list,
        description="Upstream acquisition families this one needs at least one "
        "of (computed_derivation runs over data some other family acquired). "
        "Effective availability is capped by the best of these.",
        json_schema_extra={"x_ontology_scheme": "ashcai:EvidenceMechanismScheme"},
    )
    since: str | None = Field(
        None,
        description="Platform version at which the stated availability first "
        "held, e.g. 26-R03/v0.3.0. None while planned or none.",
    )
    note: str = Field(
        ..., min_length=1,
        description="Why the value is what it is — what exists, what does not, "
        "and what would move it. Mandatory: an availability claim with no "
        "reasoning is a guess with a vocabulary.",
    )

    @model_validator(mode="after")
    def _providers_match_state(self) -> "MechanismAvailabilityEntry":
        for p in self.provided_by:
            if not re.match(COMPONENT_TOKEN_PATTERN, p):
                raise ValueError(
                    f"{self.mechanism}: provided_by {p!r} is not a component token"
                )
        best = AVAILABILITY_ORDINAL[self.availability.strongest()]
        usable = AVAILABILITY_ORDINAL[DEFAULT_MINIMUM_AVAILABILITY]
        if best >= usable and not self.provided_by:
            raise ValueError(
                f"{self.mechanism}: usable on some edition but provided_by is "
                f"empty — name the component that executes it"
            )
        if best < usable and self.since:
            raise ValueError(
                f"{self.mechanism}: `since` set but nothing is usable yet"
            )
        if EvidenceMechanism(self.mechanism) in [
            EvidenceMechanism(d) for d in self.depends_on_any
        ]:
            raise ValueError(f"{self.mechanism}: depends on itself")
        return self


class AvailabilityRecordMetadata(AshMaticsBaseModel):
    """The record_metadata header block."""

    record_id: str = Field(..., min_length=1)
    version: str = Field(
        ..., pattern=r"^\d+\.\d+\.\d+$",
        description="Record content SemVer — the value a release manifest pins.",
    )
    status: str = Field(..., description="draft | confirmed | superseded")
    generated: date
    scheme_ref: str = Field(
        ..., description="Ontology scheme the values resolve in.",
    )
    edition_ref: str = Field(
        ..., description="Where the edition axis is defined (coreapp ADR-039).",
    )
    adr_refs: list[str] = Field(..., min_length=1)
    owner: str = Field(
        ..., min_length=1,
        description="Who confirms values — a role, not a person.",
    )


class GapCause(str, Enum):
    """Why a control's assurance target exceeds what a site can reach."""

    NONE = "none"  # target is reachable; no gap
    AVAILABILITY = "availability"  # capability does not exist yet — product backlog
    ENTITLEMENT = "entitlement"  # exists, this site may not use it — licensing
    CUSTOMER = "customer"  # reachable and entitled — the customer's own work


class MechanismAvailabilityRecord(AshMaticsBaseModel):
    """The whole platform availability record: exactly one entry per
    mechanism family, so a ceiling calculation can never silently skip one."""

    record_metadata: AvailabilityRecordMetadata
    mechanisms: list[MechanismAvailabilityEntry] = Field(..., min_length=1)

    @model_validator(mode="after")
    def _one_entry_per_family(self) -> "MechanismAvailabilityRecord":
        seen = [EvidenceMechanism(m.mechanism) for m in self.mechanisms]
        dupes = {m.value for m in seen if seen.count(m) > 1}
        if dupes:
            raise ValueError(f"duplicate mechanism entries: {sorted(dupes)}")
        missing = set(EvidenceMechanism) - set(seen)
        if missing:
            raise ValueError(
                f"record is incomplete — no entry for {sorted(m.value for m in missing)}"
            )
        return self

    def entry(self, mechanism: EvidenceMechanism | str) -> MechanismAvailabilityEntry:
        m = EvidenceMechanism(mechanism)
        return next(e for e in self.mechanisms if EvidenceMechanism(e.mechanism) is m)

    @property
    def is_confirmed(self) -> bool:
        """False while the product owner has not ruled on the values. A
        ceiling computed from a draft record is provisional and a UI should
        say so; the numbers are still numbers."""
        return self.record_metadata.status == "confirmed"

    def effective_availability(
        self,
        mechanism: EvidenceMechanism | str,
        edition: Edition | str,
        deployment_mode: DeploymentMode | str | None = None,
    ) -> MechanismAvailability:
        """Own availability, capped by the best upstream family when the
        mechanism depends on one (the scheme's conjunction rule for
        computed_derivation). ``deployment_mode`` is the SOURCE system's;
        it only matters where an edition value is split by mode, and when
        unknown the weakest split value is used."""
        e = self.entry(mechanism)
        own = e.availability.for_edition(edition, deployment_mode)
        if not e.depends_on_any:
            return own
        upstream = max(
            (self.entry(d).availability.for_edition(edition, deployment_mode)
             for d in e.depends_on_any),
            key=lambda a: AVAILABILITY_ORDINAL[a],
        )
        return min(own, upstream, key=lambda a: AVAILABILITY_ORDINAL[a])

    def is_available(
        self,
        mechanism: EvidenceMechanism | str,
        edition: Edition | str,
        minimum: MechanismAvailability = DEFAULT_MINIMUM_AVAILABILITY,
        deployment_mode: DeploymentMode | str | None = None,
    ) -> bool:
        return (
            AVAILABILITY_ORDINAL[self.effective_availability(mechanism, edition, deployment_mode)]
            >= AVAILABILITY_ORDINAL[minimum]
        )

    def achievable_ceiling(
        self,
        declared: Iterable[EvidenceMechanism | str],
        edition: Edition | str,
        entitled: Callable[[EvidenceMechanism], bool] | None = None,
        minimum: MechanismAvailability = DEFAULT_MINIMUM_AVAILABILITY,
        deployment_mode: DeploymentMode | str | None = None,
    ) -> AssuranceMode:
        """The three-gate ceiling for one control.

        ``declared`` is the union of mechanisms across the control's evidence
        items at or below its maturity target (the framework gate).
        ``entitled`` is the customer gate — coreapp supplies it from tier
        settings AND site reachability (will this site's IT open the path);
        ``None`` means "assume entitled", which yields the platform ceiling.
        ``deployment_mode`` is the governed AI system's, from the registry,
        and matters only where an edition value is split by mode.
        ``human_assertion`` is the universal floor, so the result is never
        below ``attested`` even for an empty declaration.
        """
        best = AssuranceMode.ATTESTED
        for d in declared:
            m = EvidenceMechanism(d)
            if not self.is_available(m, edition, minimum, deployment_mode):
                continue
            if entitled is not None and not entitled(m):
                continue
            y = YIELDS_ASSURANCE_MODE[m]
            if ASSURANCE_ORDINAL[y] > ASSURANCE_ORDINAL[best]:
                best = y
        return best

    def diagnose_gap(
        self,
        target: AssuranceMode | str,
        declared: Iterable[EvidenceMechanism | str],
        edition: Edition | str,
        entitled: Callable[[EvidenceMechanism], bool] | None = None,
        minimum: MechanismAvailability = DEFAULT_MINIMUM_AVAILABILITY,
        deployment_mode: DeploymentMode | str | None = None,
    ) -> GapCause:
        """Which meeting a shortfall against ``target`` belongs in.

        Availability is tested before entitlement: a capability that does
        not exist cannot be licensed, so an entitlement finding is only
        meaningful once the platform gate passes.
        """
        tgt = AssuranceMode(target)
        declared = [EvidenceMechanism(d) for d in declared]
        platform_ceiling = self.achievable_ceiling(
            declared, edition, None, minimum, deployment_mode)
        if ASSURANCE_ORDINAL[platform_ceiling] < ASSURANCE_ORDINAL[tgt]:
            return GapCause.AVAILABILITY
        site_ceiling = self.achievable_ceiling(
            declared, edition, entitled, minimum, deployment_mode)
        if ASSURANCE_ORDINAL[site_ceiling] < ASSURANCE_ORDINAL[tgt]:
            return GapCause.ENTITLEMENT
        return GapCause.CUSTOMER
