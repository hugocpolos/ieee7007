"""
This module defines the Evm class, which represents the Ethical Violation management ontology
in accordance with the IEEE 7007 standard.

Module Imports:
    - IEEE7007Base: Base class for IEEE 7007 compliant models.
"""
from ieee7007.ieee7007base import IEEE7007Base


class Evm(IEEE7007Base):
    """
    Represents the EVM (Ethical Violation Management) in the context of the IEEE 7007 standard.
    Loads the bundled EVM ontology, which imports NEP and TLO.

    Parameters:
        individuals_file (str): Optional file written by `save_to_file` to continue from.
        individuals_iri (str): Optional IRI for a new individuals ontology.
    """

    def __init__(self, individuals_file=None, individuals_iri=None):
        super().__init__("evm", individuals_file=individuals_file,
                         individuals_iri=individuals_iri)
