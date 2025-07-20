"""
This module defines the Evm class, which represents the Ethical Violation management ontology
in accordance with the IEEE 7007 standard.

Module Imports:
    - IEEE7007Base: Base class for IEEE 7007 compliant models.
"""
import os

from ieee7007.ieee7007base import IEEE7007Base


class Evm(IEEE7007Base):
    """
    Represents the EVM (Ethical Violation Management) in the context of the IEEE 7007 standard.
    Inherits from the IEEE7007Base class and initializes the EVM ontology.
    """

    def __init__(self, ontology_uri=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'ontologies', 'evm.owl')):
        self.__ontology_filename = ontology_uri
        super().__init__(self.__ontology_filename)
