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
CHAR controls-catalog axis vocabularies (ontology ADR-009; aigov-framework
``controls/dev/Control-Maturity-Schema-Proposal.md``).

Five orthogonal axes describe a governance control in the CHAR catalog
(``controls/ashc_controls_catalog.yaml``) and its profiles:

- ``ControlMaturity``        how well the control is implemented
- ``AssuranceMode``          how strongly its implementation is evidenced
- ``EvidenceMechanism``      by what means that evidence is obtained
- ``MechanismAvailability``  whether Asher FORGE or a partner can execute
                             that mechanism today (a PLATFORM fact)
- ``AssuranceCadence``       how often the evidence must be refreshed

Every value is the ``skos:notation`` of exactly one concept in the matching
``ashcai:*Scheme`` in ``ashmatics-unified-ontology.ttl``, so the catalog
YAML, the profiles, the platform availability record and coreapp all
resolve to the same concept without a mapping table (ADR-006 convention).
``tests/controls/test_ontology_binding.py`` enforces membership both ways
and checks the ordinals and ``yieldsAssuranceMode`` edges against the TTL.

``Edition`` is the one axis here with no ontology anchor: it is the
commercial surface from coreapp ADR-039 (two editions, and only two), and
is recorded as PRODUCT vocabulary, not an oversight.
"""

from enum import Enum


class ControlMaturity(str, Enum):
    """``ashcai:ControlMaturityScheme`` — ordered, 1 (performed) to 5."""

    PERFORMED = "performed"
    MANAGED = "managed"
    ESTABLISHED = "established"
    PREDICTABLE = "predictable"
    OPTIMIZING = "optimizing"


class AssuranceMode(str, Enum):
    """
    ``ashcai:AssuranceModeScheme`` — ordered, 1 (attested) to 3 (collected).

    There is no ``partial``. A control instrumented for some evidence while
    an irreducible human decision stays attested is ``collected``, with the
    residual attestation named in the profile note (scheme scopeNote on
    ``ashcai:am-collected``).
    """

    ATTESTED = "attested"
    ATTESTED_WITH_ARTIFACT = "attested_with_artifact"
    COLLECTED = "collected"


class EvidenceMechanism(str, Enum):
    """
    ``ashcai:EvidenceMechanismScheme`` — the five mechanism FAMILIES. Specific
    ``evm://`` mechanisms beneath them arrive with the aigov-framework
    ``controls/evidence_mechanisms.yaml`` (queued); until then the catalog's
    evidence items and the availability record both speak at family grain.
    """

    HUMAN_ASSERTION = "human_assertion"
    DOCUMENT_SUBMISSION = "document_submission"
    SYSTEM_QUERY = "system_query"
    TELEMETRY_STREAM = "telemetry_stream"
    COMPUTED_DERIVATION = "computed_derivation"


class MechanismAvailability(str, Enum):
    """
    ``ashcai:MechanismAvailabilityScheme`` — whether the platform, or a
    partner interoperating with it, can execute a mechanism today.

    Ordered by ``ashcai:availabilityOrdinal``: none (1), planned (2),
    beta (3), generally_available (4), partner (4). ``partner`` ranks with
    ``generally_available`` because the ceiling it supports is the same;
    the delivery and commercial path differ.

    Not the release-motion "availability phase" (asher-engineering ADR-0011:
    alpha / closed beta / open beta / GA), which describes a BUILD's rollout.
    This describes a CAPABILITY. Both say "beta" and "GA" and mean different
    things, which is why the record is keyed ``mechanism_availability`` and
    never abbreviated to "availability" in a manifest.
    """

    NONE = "none"
    PLANNED = "planned"
    BETA = "beta"
    GENERALLY_AVAILABLE = "generally_available"
    PARTNER = "partner"


class AssuranceCadence(str, Enum):
    """``ashcai:AssuranceCadenceScheme`` — bounded refresh intervals, ordered
    annual (1) to intraday (6)."""

    ANNUAL = "annual"
    QUARTERLY = "quarterly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    DAILY = "daily"
    INTRADAY = "intraday"


class DeploymentMode(str, Enum):
    """
    ``ash:DeploymentModeScheme`` — where the AI SYSTEM being governed runs.
    The same axis the CLF conditions controls on (``{{system.deploymentMode}}``).

    Used here as the reach qualifier on Essentials availability: Essentials is
    Asher-hosted only, so whether FORGE can observe a source system depends on
    whether that source can reach a hosted platform at all. A cloud-hosted AI
    vendor's API can; a PACS that never leaves the firewall cannot, and the
    only way to reach it is a customer-side deployment, which is the
    Enterprise edition by definition.
    """

    CLOUD = "cloud"
    ON_PREMISE = "on_premise"
    HYBRID = "hybrid"
    EDGE = "edge"


class Edition(str, Enum):
    """
    Commercial edition, per coreapp ADR-039 Axis 1: two editions, and only
    two. One codebase serves both; they differ in which features are
    released, how the software is deployed and how it is contracted.
    Essentials is always Asher-hosted SaaS and self-serve; Enterprise is
    Asher-hosted or in the customer's own tenant, under enterprise
    procurement.

    PRODUCT vocabulary: no ontology anchor is planned. Tier (what is
    unlocked inside an edition) is deliberately NOT here — tiers are
    configuration, not an enumerated type in code (ADR-039 Axis 2), and
    entitlement is customer instance data in coreapp.
    """

    ESSENTIALS = "essentials"
    ENTERPRISE = "enterprise"


# Ordinals, mirroring ashcai:maturityOrdinal / assuranceOrdinal /
# availabilityOrdinal / cadenceOrdinal so a ceiling calculation or a UI
# compares states without hard-coding the sequence. Guard-checked against
# the TTL.
MATURITY_ORDINAL: dict[ControlMaturity, int] = {
    ControlMaturity.PERFORMED: 1,
    ControlMaturity.MANAGED: 2,
    ControlMaturity.ESTABLISHED: 3,
    ControlMaturity.PREDICTABLE: 4,
    ControlMaturity.OPTIMIZING: 5,
}

ASSURANCE_ORDINAL: dict[AssuranceMode, int] = {
    AssuranceMode.ATTESTED: 1,
    AssuranceMode.ATTESTED_WITH_ARTIFACT: 2,
    AssuranceMode.COLLECTED: 3,
}

AVAILABILITY_ORDINAL: dict[MechanismAvailability, int] = {
    MechanismAvailability.NONE: 1,
    MechanismAvailability.PLANNED: 2,
    MechanismAvailability.BETA: 3,
    MechanismAvailability.GENERALLY_AVAILABLE: 4,
    MechanismAvailability.PARTNER: 4,
}

CADENCE_ORDINAL: dict[AssuranceCadence, int] = {
    AssuranceCadence.ANNUAL: 1,
    AssuranceCadence.QUARTERLY: 2,
    AssuranceCadence.MONTHLY: 3,
    AssuranceCadence.WEEKLY: 4,
    AssuranceCadence.DAILY: 5,
    AssuranceCadence.INTRADAY: 6,
}

# ashcai:yieldsAssuranceMode — the strongest assurance mode evidence from each
# mechanism family can support. Guard-checked against the TTL edges.
YIELDS_ASSURANCE_MODE: dict[EvidenceMechanism, AssuranceMode] = {
    EvidenceMechanism.HUMAN_ASSERTION: AssuranceMode.ATTESTED,
    EvidenceMechanism.DOCUMENT_SUBMISSION: AssuranceMode.ATTESTED_WITH_ARTIFACT,
    EvidenceMechanism.SYSTEM_QUERY: AssuranceMode.COLLECTED,
    EvidenceMechanism.TELEMETRY_STREAM: AssuranceMode.COLLECTED,
    EvidenceMechanism.COMPUTED_DERIVATION: AssuranceMode.COLLECTED,
}


class SubstantiationKind(str, Enum):
    """
    ``ashcai:SubstantiationKindScheme`` — HOW a tool contract can honestly
    substantiate a claim. Ordered, 1 (attest) to 5 (connect).

    Mirrors ``EvidenceMechanism`` deliberately rather than forming an
    independent axis: a contract admits a kind, the kind yields mechanisms
    (``YIELDS_EVIDENCE_MECHANISM``), the mechanisms already carry assurance
    modes, so the achievable ceiling stays one function rather than two.

    Anchors the ``admits`` field on every entry of the aigov-framework's
    ``tooling_registry.yaml``. **That field's legal set is four values, not
    five** — see ``REGISTRY_ADMISSIBLE_KINDS``.
    """

    ATTEST = "attest"
    FORM = "form"
    CONVERSE = "converse"
    COMPUTE = "compute"
    CONNECT = "connect"


class SourceClass(str, Enum):
    """
    ``ashcai:SourceClassScheme`` — WHAT KIND of system a tool contract reads
    from. Anchors ``reads_from`` in ``tooling_registry.yaml``.

    A parallel axis to ``SubstantiationKind``, not a refinement beneath it,
    and that was measured: 8 of these 17 classes are reached by both
    ``compute`` and ``connect`` contracts, so source class varies
    independently of how the claim is substantiated.

    Unordered, flat, and no hierarchy on purpose (scheme scopeNote): a
    rollup would be at a grain nobody chose. The grain is coarse by
    decision — grouped by the connection a customer would actually make,
    not by what a tool is called, so ``LEARNING_PLATFORM`` spans LMS,
    assessment, competency and certification, and ``SERVICE_MANAGEMENT``
    spans incident intake and case management.

    Every value names a KIND of source, never a product or a system a
    customer runs. A named system is instance data and belongs in the
    coreapp Fabric binding's ``target``.
    """

    MODEL_INFERENCE = "model_inference"
    MODEL_OUTPUTS = "model_outputs"
    USAGE_TELEMETRY = "usage_telemetry"
    DATA_PLATFORM = "data_platform"
    DEPLOYED_SYSTEM = "deployed_system"
    LEARNING_PLATFORM = "learning_platform"
    COMMUNICATION_CHANNEL = "communication_channel"
    ASHER_SERVICE = "asher_service"
    SECURITY_OPERATIONS = "security_operations"
    SERVICE_MANAGEMENT = "service_management"
    API_GATEWAY = "api_gateway"
    IDENTITY_PLATFORM = "identity_platform"
    CONSENT_PLATFORM = "consent_platform"
    TERMINOLOGY_SERVICE = "terminology_service"
    SUPPLY_CHAIN_FEED = "supply_chain_feed"
    DOCUMENT_REPOSITORY = "document_repository"
    COLLABORATION_WORKSPACE = "collaboration_workspace"


# ashcai:substantiationOrdinal — the ladder, reading as increasing directness
# of evidence and increasing integration effort together. Guard-checked.
#
# NOT derived from the order values appear in a registry entry's `admits`
# list: 11 of the 135 entries author that list out of ladder order, so the
# sequence there is incidental and nothing should read it as semantic.
SUBSTANTIATION_ORDINAL: dict[SubstantiationKind, int] = {
    SubstantiationKind.ATTEST: 1,
    SubstantiationKind.FORM: 2,
    SubstantiationKind.CONVERSE: 3,
    SubstantiationKind.COMPUTE: 4,
    SubstantiationKind.CONNECT: 5,
}

# ashcai:yieldsEvidenceMechanism — one-to-MANY, unlike yieldsAssuranceMode.
# Guard-checked against the TTL edges as an exact set per kind.
#
# FORM and CONVERSE both yield DOCUMENT_SUBMISSION: converse ranks above form
# on elicitation effort, not on a stronger class of evidence.
YIELDS_EVIDENCE_MECHANISM: dict[SubstantiationKind, frozenset[EvidenceMechanism]] = {
    SubstantiationKind.ATTEST: frozenset(
        {EvidenceMechanism.HUMAN_ASSERTION, EvidenceMechanism.DOCUMENT_SUBMISSION}
    ),
    SubstantiationKind.FORM: frozenset({EvidenceMechanism.DOCUMENT_SUBMISSION}),
    SubstantiationKind.CONVERSE: frozenset({EvidenceMechanism.DOCUMENT_SUBMISSION}),
    SubstantiationKind.COMPUTE: frozenset({EvidenceMechanism.COMPUTED_DERIVATION}),
    SubstantiationKind.CONNECT: frozenset(
        {EvidenceMechanism.SYSTEM_QUERY, EvidenceMechanism.TELEMETRY_STREAM}
    ),
}

# The values a `tooling_registry.yaml` entry may legally write into `admits`.
#
# The scheme has five concepts and this set has four, and the gap is
# deliberate: EVERY contract admits ATTEST by construction, so writing it is
# redundant and the framework validator rejects it. ATTEST is still a real
# value everywhere downstream — it is the default binding for an unbuilt
# connector and the kind a ToolBinding or an ArtifactRecord most often
# carries — which is why it is a member of the enum and of the scheme.
#
# A consumer validating registry content checks membership HERE, not in
# SubstantiationKind. Do not "fix" the counts to match.
REGISTRY_ADMISSIBLE_KINDS: frozenset[SubstantiationKind] = frozenset(
    SubstantiationKind
) - {SubstantiationKind.ATTEST}
