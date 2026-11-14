"""
This module provides the IEEE7007Base class, which serves as a foundation for
managing and interacting with ontologies compliant with the IEEE 7007 standard.
It utilizes the Owlready2 library to load and manipulate ontologies and their
individuals.

Module Imports:
    - owlready2: A Python module for ontology-oriented programming.
    - logging: A standard Python module for logging messages.
    - Factory: A class for creating instances of ontology classes.
    - IndividualsLoader: A class for loading individuals from CSV files.
    - OntologyNavigator: A class for navigating the ontology structure.
"""

import logging
import os
import uuid

import owlready2

from ieee7007.factory import Factory
from ieee7007.instances_loader import IndividualsLoader
from ieee7007.navigator import OntologyNavigator

NAMESPACE = "https://w3id.org/ieee7007/"
"""Common prefix of the IRIs of the bundled ontologies and of all their terms."""

ONTOLOGIES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ontologies")

# Bundled ontologies in import order: each one imports only those before it.
_BUNDLED = ("tlo", "nep", "evm")


def ontology_iri(name):
    """
    Returns the ontology IRI of a bundled ontology.

    Parameters:
        name (str): 'tlo', 'nep' or 'evm'.

    Returns:
        str: e.g. 'https://w3id.org/ieee7007/evm'. Its terms are '<ontology IRI>#<term>'.
    """
    if name not in _BUNDLED:
        raise ValueError(f"unknown bundled ontology '{name}'")
    return NAMESPACE + name


class IEEE7007Base:
    """
    Base class for managing and interacting with ontologies compliant with the IEEE 7007 standard.

    The bundled ontologies are loaded under their own IRIs (see `ontology_iri`), from the copies
    shipped with this package, so nothing depends on where the package is installed and nothing
    is downloaded. Individuals live in a separate ontology, the *individuals ontology*, which
    imports the standard's ontology by IRI. Saving writes only the individuals ontology.
    """

    def __init__(self, ontology_name, individuals_file=None, individuals_iri=None):
        """
        Loads a bundled ontology (with its imports) and prepares the individuals ontology.

        Parameters:
            ontology_name (str): The bundled ontology to load ('evm' loads TLO, NEP and EVM).
            individuals_file (str): Optional path to a file written by `save_to_file`. Its
                ontology becomes the individuals ontology, so new individuals are added to it.
            individuals_iri (str): Optional IRI for a new individuals ontology, e.g.
                'https://example.org/my-scenario'. Ignored with `individuals_file`, which
                declares its own IRI. Defaults to a fresh 'urn:uuid:' IRI.
        """
        self._world = owlready2.World()
        self._schema = self.__load_bundled(ontology_name)
        if individuals_file is not None:
            if individuals_iri is not None:
                raise ValueError("pass either individuals_file or individuals_iri, not both")
            self._ontology = self.__load_file(individuals_file)
        else:
            self._ontology = self._world.get_ontology(individuals_iri or uuid.uuid4().urn)
            self._ontology.imported_ontologies.append(self._schema)
        self._factory = Factory(self._schema)
        self._loader = IndividualsLoader(self._ontology, self._factory)
        self.nav = OntologyNavigator(self._ontology)

    def __load_bundled(self, ontology_name):
        """
        Loads the bundled ontologies up to `ontology_name`, each under its own IRI.

        Loading them in import order means every owl:imports is already present in the world
        when it is read, so Owlready2 never tries to fetch an IRI.

        Returns:
            ontology: The loaded `ontology_name` ontology.
        """
        ontology_iri(ontology_name)  # validates the name
        ontology = None
        for name in _BUNDLED[:_BUNDLED.index(ontology_name) + 1]:
            path = os.path.join(ONTOLOGIES_DIR, f"{name}.owl")
            logging.info("Loading %s from %s", ontology_iri(name), path)
            with open(path, "rb") as fileobj:
                ontology = self._world.get_ontology(ontology_iri(name)).load(fileobj=fileobj)
        logging.info("The %s ontology has been successfully loaded", ontology_name.upper())
        return ontology

    def __load_file(self, path):
        """
        Loads a file written by `save_to_file` into the world.

        The file declares its own ontology IRI, which Owlready2 adopts; its imports of the
        bundled ontologies resolve to the copies already loaded.

        Returns:
            ontology: The loaded ontology.
        """
        logging.info("Loading individuals from %s", path)
        with open(path, "rb") as fileobj:
            return self._world.get_ontology(f"urn:uuid:{uuid.uuid4()}").load(fileobj=fileobj)

    def import_individuals_file(self, path):
        """
        Loads another file written by `save_to_file` and imports it into the individuals
        ontology, so its individuals can be linked to new ones. Its individuals keep their own
        IRIs and are not written again by `save_to_file`.

        Parameters:
            path (str): The path to the file.

        Returns:
            ontology: The loaded ontology.
        """
        ontology = self.__load_file(path)
        self._ontology.imported_ontologies.append(ontology)
        return ontology

    def load_individuals_from_file(self, individuals_file):
        """
        Loads individuals from a specified CSV file into the ontology.

        Parameters:
            individuals_file (str): The path to the CSV file containing individuals.
        """
        with self._ontology:
            self._loader.load_from_csv_file(individuals_file)

    def load_individuals_from_files(self, individuals_files):
        """
        Loads individuals from a list of specified CSV files into the ontology.

        Parameters:
            individuals_files (list of str): List of paths to the CSV files containing individuals.
        """
        with self._ontology:
            self._loader.load_from_csv_files(individuals_files)

    def new_individual(self, individual_class, individual_name):
        """
        Creates a new individual of a specified class in the ontology.

        Parameters:
            individual_class: The class of the individual to create.
            individual_name (str): The name of the individual to create.

        Returns:
            ind: The newly created individual.
        """
        with self._ontology:
            ind = self._loader.new_individual(individual_class.value, individual_name)
        return ind

    def new_property(self, property_class, source_individual, target_individual):
        """
        Establishes a property relationship between two individuals in the ontology.

        Parameters:
            property_class: The property class to use for the relationship.
            source_individual: The source individual.
            target_individual: The target individual.
        """
        with self._ontology:
            self._loader.new_property(property_class.value, source_individual, target_individual)

    def reasoning(self, verbose=False):
        """
        Executes reasoning on the ontology using the HermiT reasoner.

        Parameters:
            verbose (bool): If True, enables debug output during reasoning.
        """
        owlready2.sync_reasoner_hermit(self._world, infer_property_values=True, debug=verbose)
        logging.info("HermiT reasoner has successfully run")

    def ontology(self):
        """
        Returns the individuals ontology: the one new individuals are created in and
        `save_to_file` writes.

        Returns:
            ontology: The individuals ontology.
        """
        return self._ontology

    def schema(self):
        """
        Returns the bundled ontology this instance was created with (e.g. EVM). Its imports
        (NEP, TLO) are in `schema().imported_ontologies`.

        Returns:
            ontology: The bundled ontology.
        """
        return self._schema

    def world(self):
        """
        Returns the current ontology world.

        Returns:
            world: The current ontology world.
        """
        return self._world

    def save_to_file(self, filename):
        """
        Saves the individuals ontology to a file, as N-Triples.

        The file holds only the individuals and their relations, plus owl:imports of the
        standard's ontology (and of any `import_individuals_file` ontologies) by IRI. It contains
        no filesystem paths, so it loads on any machine with `Evm(individuals_file=...)`.

        Parameters:
            filename (str): name of the file
        """
        self.ontology().save(file=filename, format='ntriples')
