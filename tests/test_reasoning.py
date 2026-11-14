"""HermiT on the example scenario: consistent, and every inferred type is a declared, namespaced term.

The namespace check catches dangling IRIs: before they were fixed, HermiT typed individuals with
classes such as file://tlo#ActionEvent that no ontology declares.
"""
import owlready2
import pytest

from ieee7007.evm import Evm
from ieee7007.ieee7007base import NAMESPACE

EXAMPLE = "./example_data/individuals.csv"
OWL_THING = "http://www.w3.org/2002/07/owl#Thing"


@pytest.fixture(scope="module")
def reasoned():
    e = Evm(individuals_iri="https://example.org/ieee7007-tests/reasoning")
    e.load_individuals_from_file(EXAMPLE)
    e.reasoning()
    return e


def _types(individual):
    return {c.name for c in individual.INDIRECT_is_a if isinstance(c, owlready2.ThingClass)}


def test_example_is_consistent(reasoned):
    assert list(reasoned.world().inconsistent_classes()) == []


def test_inferred_types_are_declared_terms(reasoned):
    w = reasoned.world()
    inferred = {c for i in reasoned.ontology().individuals() for c in i.INDIRECT_is_a
                if isinstance(c, owlready2.ThingClass)}
    inferred |= {p for c in w.classes() for p in c.is_a if isinstance(p, owlready2.ThingClass)}
    foreign = sorted(c.iri for c in inferred if not c.iri.startswith(NAMESPACE) and c.iri != OWL_THING)
    assert foreign == []
    declared = set(w.classes())
    assert sorted(c.iri for c in inferred if c not in declared and c.iri != OWL_THING) == []


@pytest.mark.parametrize("individual, expected", [
    # NormViolation is an ActionEvent
    ("make_sound", {"NormViolation", "ActionEvent", "Event", "Occurrent"}),
    # EthicalBehaviorMonitor is an evmObject (TLO)
    ("monitor", {"EthicalBehaviorMonitor", "evmObject", "Continuant"}),
    # EventCausation is an InteractionProcess
    ("robot_malfunctioning", {"EventCausation", "InteractionProcess", "Process"}),
    # ResponsibilityAscription is a SocialInteractionProcess
    ("responsibility_ascription_robot", {"SocialInteractionProcess", "InteractionProcess"}),
    # AscriptionJustification is an InformationArtifact
    ("justification", {"AscriptionJustification", "InformationArtifact"}),
])
def test_tlo_types_are_inferred(reasoned, individual, expected):
    found = reasoned.world().search_one(iri=f"*#{individual}")
    assert expected <= _types(found)
