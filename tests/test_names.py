"""Local names since 0.3.0: no redundant ontology prefix, except where two terms would clash."""
import pytest

from ieee7007.evm import Evm
from ieee7007.ieee7007base import NAMESPACE
from ieee7007.types import IEEE7007Classes, IEEE7007Properties

KEPT = {"tloAgent", "nepAgent", "tloSituation", "nepSituation",
        "tloEnumDataTypes", "nepEnumDataTypes", "evmEnumDataTypes"}


@pytest.fixture
def evm():
    yield Evm()


def _terms(evm):
    # Owlready2 lists an entity once per ontology that declares it, so deduplicate by IRI.
    w = evm.world()
    return list({x.iri: x for x in list(w.classes()) + list(w.properties()) + list(w.individuals())
                 if x.iri.startswith(NAMESPACE)}.values())


def test_only_clashing_names_keep_their_prefix(evm):
    def prefixed(x):
        onto = x.iri[len(NAMESPACE):].split("#")[0]
        return x.name.startswith(onto)
    assert {x.name for x in _terms(evm) if prefixed(x)} == KEPT


def test_local_names_are_unique(evm):
    names = [x.name for x in _terms(evm)]
    assert len(names) == len(set(names))


def test_enum_member_names_are_unchanged():
    assert IEEE7007Classes.nepRobot.value == "Robot"
    assert IEEE7007Classes.nepAgent.value == "nepAgent"
    assert IEEE7007Properties.nepApplies.value == "applies"
    assert IEEE7007Properties.nepIsImplementedBy.value == "is_implemented_by"


@pytest.mark.parametrize("member", [
    IEEE7007Classes.evmgovernanceLevels, IEEE7007Classes.evmresponsibilityExtent,
    IEEE7007Classes.evmlegalLiabilities, IEEE7007Classes.nepnormCategory,
    IEEE7007Classes.nepnormStates, IEEE7007Classes.nepteamTypes,
    IEEE7007Classes.nepautonomousActionPrinciples, IEEE7007Classes.nepdilemmaMitigationPrinciples,
    IEEE7007Classes.nepethicalPrinciples, IEEE7007Classes.nepethicalTheories])
def test_enumeration_classes_create_individuals(evm, member):
    # These were rejected before 0.3.0 (their enum values matched no ontology name).
    individual = evm.new_individual(member, "x")
    assert member.value in [c.name for c in individual.is_a]


def test_enum_values_are_distinct():
    assert len({c.value for c in IEEE7007Classes}) == len(list(IEEE7007Classes))
    assert len({p.value for p in IEEE7007Properties}) == len(list(IEEE7007Properties))


def test_csv_accepts_current_names(evm, tmp_path):
    csv = tmp_path / "current.csv"
    csv.write_text("Robot,robot\nEthicalBehaviorMonitor,camera\nobserves,camera,robot\n")
    evm.load_individuals_from_file(str(csv))
    camera = evm.nav.get_individual_by_name("camera")
    assert [r.name for r in camera.observes] == ["robot"]


def test_csv_accepts_pre_0_3_names(evm):
    # tests/test_data uses the old prefixed names (nepRobot, evmobserves).
    evm.load_individuals_from_file("./tests/test_data/test_individuals_and_relations.csv")
    camera = evm.nav.get_individual_by_name("camera")
    assert [c.name for c in camera.is_a] == ["EthicalBehaviorMonitor"]
    assert [r.name for r in camera.observes] == ["robot"]


def test_new_property_accepts_pre_0_3_name(evm):
    robot = evm.new_individual(IEEE7007Classes.nepRobot, "robot")
    plan = evm.new_individual(IEEE7007Classes.nepAgentPlan, "plan")
    evm._loader.new_property("nepapplies", robot, plan)
    assert robot.applies == [plan]
