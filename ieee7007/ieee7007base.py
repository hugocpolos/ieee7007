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

import owlready2

from ieee7007.factory import Factory
from ieee7007.instances_loader import IndividualsLoader
from ieee7007.navigator import OntologyNavigator


class IEEE7007Base:
    """
    Base class for managing and interacting with ontologies compliant with the IEEE 7007 standard.

    This class handles the loading of ontologies, management of individuals, and reasoning tasks
    using the Owlready2 library. It encapsulates functionality for creating individuals,
    loading data from files, and running reasoners.
    """

    def __init__(self, ontology_file):
        """
        Initializes the IEEE7007Base instance with the specified ontology file.

        Parameters:
            ontology_file (str): The path to the ontology file to be loaded.
        """
        self._world = owlready2.World()
        self._ontology = self.__load_ontology(ontology_file)
        self._factory = Factory(self._ontology)
        self._loader = IndividualsLoader(self._ontology, self._factory)
        self.nav = OntologyNavigator(self._ontology)

    def __load_ontology(self, input_ontology_path):
        """
        Loads the ontology from the specified file path.

        Parameters:
            input_ontology_path (str): The path to the ontology file.

        Returns:
            ontology: The loaded ontology.
        """
        logging.info("Loading the ontology from the %s file", input_ontology_path)
        ontology = self._world.get_ontology(input_ontology_path)
        ontology.load()
        logging.info("The EVM ontology has been successfully loaded")
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
        Returns the currently loaded ontology.

        Returns:
            ontology: The loaded ontology.
        """
        return self._ontology

    def world(self):
        """
        Returns the current ontology world.

        Returns:
            world: The current ontology world.
        """
        return self._world

    def save_to_file(self, filename):
        """
        Save the ontology to an owl file.

        Parameters:
            filename (str): name of the file
        """
        self.ontology().save(file=filename, format='ntriples')
