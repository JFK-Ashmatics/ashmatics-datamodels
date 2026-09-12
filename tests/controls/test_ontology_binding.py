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
ADR-002 binding guard for the controls axis vocabularies (ontology ADR-009).

Every enum value is a ``skos:notation`` in its ``ashcai:*Scheme``, both
directions (no drift either way); the ordinal tables match the ontology's
``maturityOrdinal`` / ``assuranceOrdinal`` / ``availabilityOrdinal``; and
``YIELDS_ASSURANCE_MODE`` matches the ``ashcai:yieldsAssuranceMode`` edges.
The framework validator keeps an inline mirror of the same dicts
(validate_controls_catalog.py) so it has no ontology runtime dependency;
this guard is what keeps that mirror honest by construction.

``Edition`` is PRODUCT vocabulary (coreapp ADR-039) and deliberately has no
scheme; it is asserted absent here so a future anchor is a decision.
"""

import os
from enum import Enum
from pathlib import Path

import pytest

pytest.importorskip("rdflib")
from rdflib import RDF, Graph, URIRef  # noqa: E402
from rdflib.namespace import SKOS  # noqa: E402

from ashmatics_datamodels.controls import (  # noqa: E402
    ASSURANCE_ORDINAL,
    AVAILABILITY_ORDINAL,
    CADENCE_ORDINAL,
    MATURITY_ORDINAL,
    REGISTRY_ADMISSIBLE_KINDS,
    SUBSTANTIATION_ORDINAL,
    YIELDS_ASSURANCE_MODE,
    YIELDS_EVIDENCE_MECHANISM,
    AssuranceCadence,
    AssuranceMode,
    ControlMaturity,
    DeploymentMode,
    Edition,
    EvidenceMechanism,
    MechanismAvailability,
    SourceClass,
    SubstantiationKind,
)

ASHCAI = "https://ashmatics.com/ontology/cai#"
ASH = "http://asherinformatics.com/ontology/ashmatics/"
ONTOLOGY_FILE = "ashmatics-unified-ontology.ttl"

# scheme IRIs; the five control axes are ashcai:, the reach qualifier is ash:
SCHEMES: dict[type[Enum], str] = {
    ControlMaturity: ASHCAI + "ControlMaturityScheme",
    AssuranceMode: ASHCAI + "AssuranceModeScheme",
    EvidenceMechanism: ASHCAI + "EvidenceMechanismScheme",
    MechanismAvailability: ASHCAI + "MechanismAvailabilityScheme",
    AssuranceCadence: ASHCAI + "AssuranceCadenceScheme",
    DeploymentMode: ASH + "DeploymentModeScheme",
    SubstantiationKind: ASHCAI + "SubstantiationKindScheme",
    SourceClass: ASHCAI + "SourceClassScheme",
}
ORDINALS: dict[type[Enum], tuple[dict, str]] = {
    ControlMaturity: (MATURITY_ORDINAL, "maturityOrdinal"),
    AssuranceMode: (ASSURANCE_ORDINAL, "assuranceOrdinal"),
    MechanismAvailability: (AVAILABILITY_ORDINAL, "availabilityOrdinal"),
    AssuranceCadence: (CADENCE_ORDINAL, "cadenceOrdinal"),
    SubstantiationKind: (SUBSTANTIATION_ORDINAL, "substantiationOrdinal"),
}


def _ontology_dir() -> Path | None:
    env = os.environ.get("ASHMATICS_ONTOLOGY_DIR")
    if env:
        p = Path(env).expanduser()
        return p if p.is_dir() else None
    sibling = Path(__file__).resolve().parents[2].parent / "ashmatics-ontology"
    return sibling if sibling.is_dir() else None


@pytest.fixture(scope="module")
def graph() -> Graph:
    d = _ontology_dir()
    if d is None or not (d / ONTOLOGY_FILE).is_file():
        pytest.skip("ontology source not found; set ASHMATICS_ONTOLOGY_DIR or check out "
                    "ashmatics-ontology beside this repo")
    g = Graph()
    g.parse(d / ONTOLOGY_FILE, format="turtle")
    return g


def _concepts(g: Graph, scheme: str) -> dict[str, URIRef]:
    s = URIRef(scheme if scheme.startswith("http") else ASHCAI + scheme)
    out: dict[str, URIRef] = {}
    for c in set(g.subjects(RDF.type, s)) | set(g.subjects(SKOS.inScheme, s)):
        for n in g.objects(c, SKOS.notation):
            out[str(n)] = c
    return out


@pytest.mark.parametrize("enum_type", list(SCHEMES))
def test_enum_values_are_exactly_the_scheme_notations(graph, enum_type):
    notations = _concepts(graph, SCHEMES[enum_type])
    assert notations, f"{SCHEMES[enum_type]} has no concepts with skos:notation"
    values = {m.value for m in enum_type}
    assert values == set(notations), (
        f"{enum_type.__name__} vs ashcai:{SCHEMES[enum_type]}: "
        f"enum-only {sorted(values - set(notations))}, "
        f"ontology-only {sorted(set(notations) - values)}"
    )


@pytest.mark.parametrize("enum_type", list(ORDINALS))
def test_ordinals_match_ontology(graph, enum_type):
    table, prop = ORDINALS[enum_type]
    notations = _concepts(graph, SCHEMES[enum_type])
    for member in enum_type:
        vals = list(graph.objects(notations[member.value], URIRef(ASHCAI + prop)))
        assert vals, f"{member} carries no ashcai:{prop} in the ontology"
        assert int(vals[0]) == table[member], (
            f"{enum_type.__name__}.{member.name}: ordinal {table[member]} != "
            f"ontology {int(vals[0])}"
        )


def test_yields_assurance_mode_matches_ontology(graph):
    mechs = _concepts(graph, "EvidenceMechanismScheme")
    modes = {v: k for k, v in _concepts(graph, "AssuranceModeScheme").items()}
    for mech, mode in YIELDS_ASSURANCE_MODE.items():
        edges = list(graph.objects(mechs[mech.value], URIRef(ASHCAI + "yieldsAssuranceMode")))
        assert len(edges) == 1, f"{mech.value}: expected one yieldsAssuranceMode edge"
        assert modes[edges[0]] == mode.value, (
            f"{mech.value} yields {mode.value} in code, {modes[edges[0]]} in the ontology"
        )


def test_edition_has_no_ontology_anchor(graph):
    """PRODUCT vocabulary by decision (coreapp ADR-039). The notation
    `enterprise` does exist in the ontology — as ashcai:es-enterprise in
    EngagementScope (enterprise vs use_case), a different axis — so the test
    is for a scheme carrying BOTH editions. If one lands, bind it and retire
    this assertion."""
    wanted = {m.value for m in Edition}
    for scheme in set(graph.objects(None, SKOS.inScheme)):
        notations = {
            str(n)
            for c in graph.subjects(SKOS.inScheme, scheme)
            for n in graph.objects(c, SKOS.notation)
        }
        assert not wanted <= notations, f"{scheme} now carries the editions; bind Edition to it"


def test_yields_evidence_mechanism_matches_ontology(graph):
    """
    ``ashcai:yieldsEvidenceMechanism``, checked as an exact SET per kind.

    Unlike ``yieldsAssuranceMode`` this edge is one-to-many, so a
    len-1 assertion would not fit and a subset assertion would let the
    ontology grow an edge the ceiling calculation never sees.
    """
    kinds = _concepts(graph, "SubstantiationKindScheme")
    mechs = {v: k for k, v in _concepts(graph, "EvidenceMechanismScheme").items()}
    prop = URIRef(ASHCAI + "yieldsEvidenceMechanism")
    for kind, expected in YIELDS_EVIDENCE_MECHANISM.items():
        edges = {mechs[o] for o in graph.objects(kinds[kind.value], prop)}
        assert edges == {m.value for m in expected}, (
            f"{kind.value} yields {sorted(m.value for m in expected)} in code, "
            f"{sorted(edges)} in the ontology"
        )


def test_registry_admissible_kinds_is_the_scheme_minus_attest(graph):
    """
    The scheme has five concepts; ``tooling_registry.yaml``'s ``admits``
    field legally carries four.

    Every contract admits ``attest`` by construction, so writing it is
    redundant and the framework validator rejects it. This asserts the gap
    stays exactly one concept and exactly that one, so nobody "reconciles"
    the counts in either direction: dropping ATTEST from the enum would
    break the scheme parity test above, and adding it here would start
    accepting a listed ``attest`` in the registry.
    """
    notations = set(_concepts(graph, "SubstantiationKindScheme"))
    admissible = {k.value for k in REGISTRY_ADMISSIBLE_KINDS}
    assert notations - admissible == {"attest"}
    assert admissible < notations


def test_source_class_scheme_is_flat(graph):
    """
    ``ashcai:SourceClassScheme`` carries no ``skos:broader``, deliberately:
    a hierarchy would let a consumer roll up at a grain nobody chose
    (handoff spec, and the scheme's own scopeNote).
    """
    scheme = URIRef(SCHEMES[SourceClass])
    concepts = list(graph.subjects(SKOS.inScheme, scheme))
    # Not vacuous: an unresolvable scheme IRI would give an empty loop, which
    # is indistinguishable from a pass.
    assert len(concepts) == len(list(SourceClass))
    for c in concepts:
        assert not list(graph.objects(c, SKOS.broader)), f"{c} has skos:broader"


def test_no_reads_from_source_class_property(graph):
    """
    Which tool reads from what is REGISTRY content, held on the tool entry
    in CHAR. The ontology supplies the vocabulary and nothing more; minting
    the property would invite asserting instance relations in TTL.
    """
    assert not list(graph.subjects(RDF.type, URIRef(ASHCAI + "readsFromSourceClass")))
    assert not list(graph.predicate_objects(URIRef(ASHCAI + "readsFromSourceClass")))
