"""IRIs: the bundled ontologies and saved files must not depend on where things are installed."""
import os
import shutil
import subprocess
import sys

import pytest

from ieee7007.evm import Evm
from ieee7007.ieee7007base import NAMESPACE, ONTOLOGIES_DIR, ontology_iri
from ieee7007.types import IEEE7007Classes, IEEE7007Properties

TREE_IRI = "https://example.org/nav2-to-onto/tree"
RUN_IRI = "https://example.org/nav2-to-onto/run"


@pytest.fixture
def evm():
    yield Evm()


def test_bundled_ontologies_have_stable_iris(evm):
    assert evm.schema().base_iri == ontology_iri("evm") + "#"
    assert sorted(o.base_iri for o in evm.schema().imported_ontologies) == [
        ontology_iri("nep") + "#", ontology_iri("tlo") + "#"]


def test_terms_live_in_the_namespace(evm):
    w = evm.world()
    assert w.search_one(iri=NAMESPACE + "nep#AgentPlan") is not None
    assert w.search_one(iri=NAMESPACE + "nep#applies") is not None
    assert w.search_one(iri=NAMESPACE + "tlo#ActionEvent") is not None
    assert w.search_one(iri=NAMESPACE + "evm#NormViolation") is not None
    foreign = [e.iri for e in list(w.classes()) + list(w.properties()) + list(w.individuals())
               if not e.iri.startswith(NAMESPACE) and not e.iri.startswith("http://www.w3.org/")
               and not e.iri.startswith("http://purl.org/")]
    assert foreign == []


def test_every_enum_member_exists(evm):
    assert [c.value for c in IEEE7007Classes if evm._factory.get_factory_by_name(c.value) is None] == []
    resolved = [evm._factory.get_factory_by_name(c.value) for c in IEEE7007Classes]
    assert [c.iri for c in resolved if not c.iri.startswith(NAMESPACE)] == []
    properties = {p.name: p for p in evm.world().properties()}
    assert [p.value for p in IEEE7007Properties if p.value not in properties] == []
    assert [p.value for p in IEEE7007Properties
            if not properties[p.value].iri.startswith(NAMESPACE)] == []


def test_bundled_files_contain_no_file_iris():
    for name in ("tlo", "nep", "evm"):
        with open(os.path.join(ONTOLOGIES_DIR, f"{name}.owl"), encoding="utf-8") as fh:
            text = fh.read()
        assert "file://" not in text, name


def test_new_individuals_go_in_the_individuals_ontology():
    e = Evm(individuals_iri=TREE_IRI)
    robot = e.new_individual(IEEE7007Classes.nepRobot, "robot")
    assert robot.iri == TREE_IRI + "#robot"
    assert robot.namespace.ontology is e.ontology()


def test_default_individuals_iri_is_a_uuid_urn(evm):
    assert evm.ontology().base_iri.startswith("urn:uuid:")


def test_individuals_file_and_iri_are_exclusive(tmp_path):
    path = tmp_path / "x.nt"
    Evm(individuals_iri=TREE_IRI).save_to_file(str(path))
    with pytest.raises(ValueError):
        Evm(individuals_file=str(path), individuals_iri=TREE_IRI)


def test_saved_file_has_only_individuals_and_no_paths(tmp_path):
    e = Evm(individuals_iri=TREE_IRI)
    robot = e.new_individual(IEEE7007Classes.nepRobot, "robot")
    plan = e.new_individual(IEEE7007Classes.nepAgentPlan, "plan")
    e.new_property(IEEE7007Properties.nepApplies, robot, plan)
    path = tmp_path / "tree.nt"
    e.save_to_file(str(path))
    text = path.read_text(encoding="utf-8")

    assert "file://" not in text
    assert ONTOLOGIES_DIR not in text and str(tmp_path) not in text and os.getcwd() not in text
    assert f"<{TREE_IRI}> <http://www.w3.org/2002/07/owl#imports> <{ontology_iri('evm')}>" in text
    assert f"<{TREE_IRI}#robot> <{NAMESPACE}nep#applies> <{TREE_IRI}#plan>" in text
    # The schema is imported, not copied: no class declarations in the file.
    assert "owl#Class>" not in text
    assert len(text.splitlines()) < 20


def test_saved_file_loads_elsewhere(tmp_path):
    """Save, copy to another directory, and load it in a fresh interpreter started there."""
    e = Evm(individuals_iri=TREE_IRI)
    robot = e.new_individual(IEEE7007Classes.nepRobot, "robot")
    plan = e.new_individual(IEEE7007Classes.nepAgentPlan, "plan")
    e.new_property(IEEE7007Properties.nepApplies, robot, plan)
    e.save_to_file(str(tmp_path / "tree.nt"))
    other = tmp_path / "other"
    other.mkdir()
    shutil.copy(tmp_path / "tree.nt", other / "moved.nt")

    code = (
        "from ieee7007.evm import Evm\n"
        "e = Evm(individuals_file='moved.nt')\n"
        f"assert e.ontology().base_iri == '{TREE_IRI}#'\n"
        "robot = e.world().search_one(iri='*#robot')\n"
        "assert [c.name for c in robot.is_a] == ['Robot']\n"
        "assert [p.name for p in robot.applies] == ['plan']\n"
        "print('ok')\n")
    out = subprocess.run([sys.executable, "-c", code], cwd=other, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "ok"


def test_import_individuals_file_links_without_copying(tmp_path):
    tree = Evm(individuals_iri=TREE_IRI)
    tree.new_individual(IEEE7007Classes.nepPlanAction, "follow_path")
    tree.save_to_file(str(tmp_path / "tree.nt"))

    run = Evm(individuals_iri=RUN_IRI)
    run.import_individuals_file(str(tmp_path / "tree.nt"))
    occurrence = run.new_individual(IEEE7007Classes.nepAgentAction, "occ_1")
    run.new_property(IEEE7007Properties.nepIsImplementedBy, "follow_path", occurrence)
    run.save_to_file(str(tmp_path / "run.nt"))
    text = (tmp_path / "run.nt").read_text(encoding="utf-8")

    assert f"<{RUN_IRI}> <http://www.w3.org/2002/07/owl#imports> <{TREE_IRI}>" in text
    assert f"<{TREE_IRI}#follow_path> <{NAMESPACE}nep#is_implemented_by> <{RUN_IRI}#occ_1>" in text
    # The tree's own individual is not written again.
    assert f"<{TREE_IRI}#follow_path> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>" not in text


def test_version_iris_match_package_version(evm):
    import tomllib
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "pyproject.toml"), "rb") as fh:
        version = tomllib.load(fh)["project"]["version"]
    for name in ("tlo", "nep", "evm"):
        with open(os.path.join(ONTOLOGIES_DIR, f"{name}.owl"), encoding="utf-8") as fh:
            text = fh.read()
        assert f'<owl:versionIRI rdf:resource="{NAMESPACE}{version}/{name}"/>' in text, name
