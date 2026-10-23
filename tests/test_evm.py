import importlib.util
import os

import pytest

from ieee7007.evm import Evm
from ieee7007.types import IEEE7007Classes, IEEE7007Properties

HAS_PLOT_EXTRA = all(importlib.util.find_spec(m) for m in ('networkx', 'matplotlib', 'pygraphviz'))
requires_plot = pytest.mark.skipif(not HAS_PLOT_EXTRA, reason="needs the 'plot' extra")


@pytest.fixture
def evm():
    yield Evm()


@pytest.fixture
def file_operation(request):
    def finalizer():
        os.remove('test_onto.owl')

    request.addfinalizer(finalizer)
    return dict(filename='test_onto.owl')


def individual_exists(individual_name, e):
    return individual_name in [x.name for x in e.ontology().individuals()]


def number_of_individuals(e):
    return len(list(e.ontology().individuals()))


def test_load_evm(evm):
    assert evm is not None


def test_load_evm_and_load_individual_from_a_single_file(evm):
    number_of_individuals_before = number_of_individuals(evm)
    evm.load_individuals_from_file('./tests/test_data/single_individual.csv')
    assert number_of_individuals(evm) == number_of_individuals_before + 1


def test_load_evm_and_load_individual_from_multiple_files(evm):
    number_of_individuals_before = number_of_individuals(evm)
    evm.load_individuals_from_files(
        ['./tests/test_data/single_individual.csv', './tests/test_data/two_individuals.csv'])
    assert number_of_individuals(evm) == number_of_individuals_before + 3


def test_load_instance_manually_by_name(evm):
    number_of_individuals_before = number_of_individuals(evm)
    assert not individual_exists('robot1', evm)
    evm.new_individual(IEEE7007Classes.nepRobot, 'robot1')
    assert number_of_individuals(evm) == number_of_individuals_before + 1
    assert individual_exists('robot1', evm)
    assert not individual_exists('camera1', evm)
    evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera1')
    assert number_of_individuals(evm) == number_of_individuals_before + 2
    assert individual_exists('camera1', evm)


def test_load_instance_manually_by_instance(evm):
    robot1 = evm.new_individual(IEEE7007Classes.nepRobot, 'robot1')
    assert robot1.name == 'robot1'
    assert 'nepRobot' in [x.name for x in robot1.is_a]
    camera1 = evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera1')
    assert camera1.name == 'camera1'
    assert 'evmEthicalBehaviorMonitor' in [x.name for x in camera1.is_a]


def test_load_instance_property_manually_by_name(evm):
    evm.new_individual(IEEE7007Classes.nepRobot, 'robot1')
    evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera1')
    evm.new_property(IEEE7007Properties.evmObserves, 'camera1', 'robot1')

    camera1 = evm.nav.get_individual_by_name('camera1')
    assert camera1 is not None
    relations = evm.nav.get_all_properties_relations_of_an_individual(camera1)
    assert relations is not None
    assert len(relations) == 1
    assert relations[0].prop.name == 'evmobserves'
    assert relations[0].source.name == 'camera1'
    assert relations[0].target.name == 'robot1'


def test_load_instance_property_manually_by_instance(evm):
    robot1 = evm.new_individual(IEEE7007Classes.nepRobot, 'robot1')
    camera1 = evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera1')
    evm.new_property(IEEE7007Properties.evmObserves, camera1, robot1)
    relations = evm.nav.get_all_properties_relations_of_an_individual(camera1)
    assert relations[0].source == camera1
    assert relations[0].target == robot1


def test_load_and_save_ontology_on_new_file(evm, file_operation):
    filename = file_operation.get('filename')
    evm.save_to_file(filename)
    assert os.path.isfile(filename)
    assert os.path.getsize(filename) > 0


def test_save_ontology_with_new_individuals(evm, file_operation):
    filename = file_operation.get('filename')
    evm.new_individual(IEEE7007Classes.nepRobot, 'robot1')
    evm.new_individual(IEEE7007Classes.nepRobot, 'robot2')
    evm.new_individual(IEEE7007Classes.nepNorm, 'do not hit the wall')
    evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera')
    evm.save_to_file(filename)
    assert os.path.isfile(filename)
    assert os.path.getsize(filename) > 0


def test_save_ontology_with_new_individual_relations(evm, file_operation):
    filename = file_operation.get('filename')
    evm.new_individual(IEEE7007Classes.nepRobot, 'robot1')
    evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera')
    evm.new_property(IEEE7007Properties.evmObserves, "camera", "robot1")
    evm.save_to_file(filename)
    assert os.path.isfile(filename)
    assert os.path.getsize(filename) > 0


def test_load_an_ontology_from_a_modified_file(evm, file_operation):
    filename = file_operation.get('filename')
    robot = evm.new_individual(IEEE7007Classes.nepRobot, 'robot_name')
    camera = evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera')
    evm.new_property(IEEE7007Properties.evmObserves, camera, robot)
    evm.save_to_file(filename)

    new_evm = Evm(filename)
    new_robot = new_evm.nav.get_individual_by_name('robot_name')
    assert new_robot is not None
    assert new_robot != robot
    assert new_robot.name == 'robot_name'

    new_camera = new_evm.nav.get_individual_by_name('camera')
    assert new_camera is not None
    assert new_camera != camera
    assert new_camera.name == 'camera'

    new_robot in new_camera.evmobserves


def test_reasoning(evm):
    number_of_individuals = evm.nav.get_number_of_individuals()
    evm.reasoning()
    assert evm.nav.get_number_of_individuals() == number_of_individuals
    number_of_individuals = evm.nav.get_number_of_individuals()
    robot = evm.new_individual(IEEE7007Classes.nepRobot, 'robot_name')
    camera = evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera')
    evm.new_property(IEEE7007Properties.evmObserves, camera, robot)
    evm.reasoning()
    assert evm.nav.get_number_of_individuals() == number_of_individuals + 2


def test_reasoning_and_saving_the_ontology(evm, file_operation):
    filename = file_operation.get('filename')
    robot = evm.new_individual(IEEE7007Classes.nepRobot, 'robot_name')
    camera = evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera')
    evm.new_property(IEEE7007Properties.evmObserves, camera, robot)
    evm.reasoning()
    evm.save_to_file(filename)
    assert os.path.isfile(filename)
    assert os.path.getsize(filename) > 0


def test_dump_ontology(evm):
    robot = evm.new_individual(IEEE7007Classes.nepRobot, 'robot')
    camera = evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera')
    evm.new_property(IEEE7007Properties.evmObserves, camera, robot)
    evm.reasoning()
    evm.nav.dump_ontology()


@pytest.mark.skipif(HAS_PLOT_EXTRA, reason="plot extra is installed")
def test_plot_without_extra_raises(evm):
    with pytest.raises(ImportError, match=r"ieee7007\[plot\]"):
        evm.nav.plot(False)


@requires_plot
def test_plot_ontology(evm):
    robot = evm.new_individual(IEEE7007Classes.nepRobot, 'robot')
    camera = evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera')
    evm.new_property(IEEE7007Properties.evmObserves, camera, robot)
    evm.reasoning()
    evm.nav.plot(False)


@requires_plot
def test_plot_ontology2(evm):
    evm.load_individuals_from_file('./example_data/individuals.csv')
    evm.reasoning()
    evm.nav.plot(False)


@requires_plot
def test_plot_individual(evm):
    robot = evm.new_individual(IEEE7007Classes.nepRobot, 'robot')
    camera = evm.new_individual(IEEE7007Classes.evmEthicalBehaviorMonitor, 'camera')
    evm.new_property(IEEE7007Properties.evmObserves, camera, robot)
    evm.reasoning()
    evm.nav.plot_individual(robot, draw=False)
    evm.nav.plot_individual(camera, draw=False)


@requires_plot
def test_plot_more_individuals(evm):
    evm.load_individuals_from_file('./example_data/individuals.csv')
    evm.reasoning()
    for ind in evm.nav.all_individuals:
        evm.nav.plot_individual(ind)
