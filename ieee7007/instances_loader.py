"""
instances_loader.py

This module is responsible for loading instances of both individuals and properties over the
ontological standards defined on IEEE7007.
It includes functions and classes that handle the load of individual and properties.
"""

import csv
import os.path

from ieee7007.types import IEEE7007InvalidClass, IEEE7007InvalidProperty


class InvalidOntologyCSVFile(Exception):
    """
    Exception raised for errors in the ontology CSV file format.

    This exception is used to indicate that the provided CSV file does
    not conform to the expected format for ontology data, allowing
    for better error handling and debugging.
    """


class IndividualsLoader:
    """
    A class to load individuals and their properties from CSV files into an ontology.

    This class handles the loading of individuals and their relationships from
    specified CSV files, validating the input and raising appropriate exceptions
    for any issues encountered during the loading process.
    """

    def __init__(self, ontology, factory):
        """
        Initializes the IndividualsLoader with the given ontology and factory.

        Args:
            ontology: An instance of the ontology to load individuals into.
            factory: A factory for creating new individuals and properties.
        """
        self._ontology = ontology
        self._factory = factory

    def load_from_csv_files(self, files):
        """
        Loads individuals and properties from a list of CSV files.

        Args:
            files: A list of file paths to the CSV files containing individuals
                   and properties.
        """
        for file in files:
            self.load_from_csv_file(file)

    def load_from_csv_file(self, file):
        """
        Loads individuals and properties from a single CSV file.

        Args:
            file: The path to the CSV file to be loaded.

        Raises:
            InvalidOntologyCSVFile: If the file is not found or if there are
            issues with the contents of the file.
        """
        if not os.path.isfile(file):
            raise InvalidOntologyCSVFile(f"{file} not found.")

        with open(file, 'r', encoding='utf-8') as fp:
            reader = csv.reader(fp)

            for i, line in enumerate(reader):
                if self._empty_line(line):
                    continue

                if self._is_commentary(line):
                    continue

                if self._is_individual(line):
                    try:
                        self._load_individual_csv_line(line)
                    except ValueError as err:
                        raise InvalidOntologyCSVFile(
                            f"{file}:{i+1}. Error loading individual {err}") from err

                elif self._is_property(line):
                    try:
                        self._load_property_csv_line(line)
                    except ValueError as err:
                        raise InvalidOntologyCSVFile(
                            f"{file}:{i+1}. Error loading property {err}") from err
                else:
                    raise InvalidOntologyCSVFile(
                        f"{file}: {i+1}. Invalid line(number of columns: {len(line)})")

    def new_individual(self, class_name, individual_name):
        """
        Creates a new individual in the ontology.

        Args:
            class_name: The name of the class the individual belongs to.
            individual_name: The name of the individual to be created.

        Returns:
            The newly created individual.

        Raises:
            IEEE7007InvalidClass: If the class name is invalid.
        """
        f = self._factory.get_factory_by_name(class_name)
        if f is None:
            raise IEEE7007InvalidClass(f"Invalid class '{class_name}'")
        return f(individual_name)

    def new_property(self, property_class, source, target):
        """
        Creates a new property relationship between individuals.

        Args:
            property_class: The class of the property being created.
            source: The source individual (can be a string name or an individual).
            target: The target individual (can be a string name or an individual).

        Raises:
            ValueError: The individual does not exist.
            IEEE7007InvalidProperty: The property does not exist in the source individual.
        """
        if isinstance(source, str):
            source_individual = self._get_ontology_individual_by_name(source)
        else:
            source_individual = source

        if source_individual is None:
            raise ValueError(f"individual '{source}' does not exist")

        if isinstance(target, str):
            target_individual = self._get_ontology_individual_by_name(target)
        else:
            target_individual = target

        if source_individual is None:
            raise ValueError(f"individual '{target}' does not exist")

        if not hasattr(source_individual, property_class):
            raise IEEE7007InvalidProperty(
                f"""property '{property_class}' does not exist in the class
                    '{source_individual.is_a[0]}'""")

        source_property = getattr(source_individual, property_class)
        if property_class in ['nepcategory', 'nepteam_type']:
            setattr(source_individual, property_class, target_individual)
        else:
            source_property.append(target_individual)

    def _empty_line(self, csv_line: list):
        """
        Checks if a given CSV line is empty.

        Args:
            csv_line: The line to check.

        Returns:
            True if the line is empty, False otherwise.
        """
        return len(csv_line) == 0

    def _is_commentary(self, csv_line: list):
        """
        Checks if a given CSV line is a commentary.

        Args:
            csv_line: The line to check.

        Returns:
            True if the line is a commentary, False otherwise.
        """
        return csv_line[0].startswith('/*') and csv_line[-1].endswith('*/')

    def _is_individual(self, csv_line):
        """
        Checks if a given CSV line represents an individual.

        Args:
            csv_line: The line to check.

        Returns:
            True if the line represents an individual, False otherwise.
        """
        return len(csv_line) == 2

    def _is_property(self, csv_line):
        """
        Checks if a given CSV line represents a property.

        Args:
            csv_line: The line to check.

        Returns:
            True if the line represents a property, False otherwise.
        """
        return len(csv_line) == 3

    def _load_individual_csv_line(self, line):
        """
        Loads an individual from a CSV line.

        Args:
            line: The line containing the class name and individual name.

        Returns:
            The newly created individual.
        """
        class_name, individual_name = line
        return self.new_individual(class_name, individual_name)

    def _load_property_csv_line(self, line):
        """
        Loads a property from a CSV line.

        Args:
            line: The line containing the property name, source, and target.

        Returns:
            The newly created property relationship.
        """
        property_name, source, target = line
        return self.new_property(property_name, source, target)

    def _get_ontology_individual_by_name(self, individual_name):
        """
        Retrieves an ontology individual by name.

        Args:
            individual_name: The name of the individual to retrieve.

        Returns:
            The individual if found, None otherwise.
        """
        for i in self._ontology.world.individuals():
            if i.name == individual_name:
                return i
        return None
