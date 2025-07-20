import pytest

from ieee7007.instances_loader import IndividualsLoader, InvalidOntologyCSVFile
from ieee7007.factory import Factory
from tests.fake_ontology import FakeOntology


def test_empty_loader():
    ld = IndividualsLoader(None, None)

    with pytest.raises(InvalidOntologyCSVFile):
        ld.load_from_csv_file('')

    with pytest.raises(AttributeError):
        ld.load_from_csv_file('./tests/test_data/single_individual.csv')


def test_loader_only_individuals():
    f = Factory(FakeOntology())
    ld = IndividualsLoader(None, f)

    with pytest.raises(InvalidOntologyCSVFile):
        ld.load_from_csv_file('')

    ld.load_from_csv_file('./tests/test_data/single_individual.csv')

