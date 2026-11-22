"""new_property sets functional properties (at most one value) instead of appending to them."""
import owlready2
import pytest

from ieee7007.evm import Evm
from ieee7007.types import IEEE7007Classes, IEEE7007InvalidProperty, IEEE7007Properties


@pytest.fixture
def evm():
    yield Evm()


def _enum(evm, name):
    return evm.world().search_one(iri=f"*#{name}")


def test_all_functional_properties_are_known(evm):
    # If the schema gains or loses a functional property, revisit the tests below.
    functional = {p.name for p in evm.world().properties()
                  if owlready2.FunctionalProperty in p.is_a}
    assert functional == {"state", "category", "team_type", "maturity", "scope"}


def test_state_is_set(evm):
    obligation = evm.new_individual(IEEE7007Classes.nepObligation, "obligation")
    evm.new_property(IEEE7007Properties.nepState, obligation, _enum(evm, "activated"))
    assert obligation.state == _enum(evm, "activated")


def test_state_is_replaced(evm):
    obligation = evm.new_individual(IEEE7007Classes.nepObligation, "obligation")
    evm.new_property(IEEE7007Properties.nepState, obligation, _enum(evm, "activated"))
    evm.new_property(IEEE7007Properties.nepState, obligation, _enum(evm, "fulfilled"))
    assert obligation.state == _enum(evm, "fulfilled")


def test_state_by_names(evm):
    evm.new_individual(IEEE7007Classes.nepObligation, "obligation")
    evm.new_property(IEEE7007Properties.nepState, "obligation", "violated")
    assert evm.nav.get_individual_by_name("obligation").state == _enum(evm, "violated")


def test_state_survives_save_and_reload(evm, tmp_path):
    obligation = evm.new_individual(IEEE7007Classes.nepObligation, "obligation")
    evm.new_property(IEEE7007Properties.nepState, obligation, _enum(evm, "suspended"))
    path = tmp_path / "individuals.nt"
    evm.save_to_file(str(path))
    reloaded = Evm(individuals_file=str(path))
    assert reloaded.nav.get_individual_by_name("obligation").state.name == "suspended"


def test_category_still_set(evm):
    norm = evm.new_individual(IEEE7007Classes.nepObligation, "obligation")
    evm.new_property(IEEE7007Properties.nepCategory, norm, _enum(evm, "ethical_norm"))
    assert norm.category == _enum(evm, "ethical_norm")


def test_non_functional_property_still_appends(evm):
    robot = evm.new_individual(IEEE7007Classes.nepRobot, "robot")
    p1 = evm.new_individual(IEEE7007Classes.nepAgentPlan, "p1")
    p2 = evm.new_individual(IEEE7007Classes.nepAgentPlan, "p2")
    evm.new_property(IEEE7007Properties.nepApplies, robot, p1)
    evm.new_property(IEEE7007Properties.nepApplies, robot, p2)
    assert robot.applies == [p1, p2]


def test_missing_target_raises(evm):
    robot = evm.new_individual(IEEE7007Classes.nepRobot, "robot")
    with pytest.raises(ValueError, match="does_not_exist"):
        evm.new_property(IEEE7007Properties.nepApplies, robot, "does_not_exist")


def test_non_property_attribute_raises(evm):
    robot = evm.new_individual(IEEE7007Classes.nepRobot, "robot")
    plan = evm.new_individual(IEEE7007Classes.nepAgentPlan, "plan")
    with pytest.raises(IEEE7007InvalidProperty):
        evm._loader.new_property("name", robot, plan)
