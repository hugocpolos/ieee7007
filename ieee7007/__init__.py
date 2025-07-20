"""
ieee7007.__init__

Description:
    This package provides a collection of functionalities to work with the ontological patterns
    proposed on the IEEE7007 2021 Documents. It makes it easier to load an ontological scenario
    modeled over the EVM (Ethical Violation Management) and NEP (Norms and principles) ontologies.

Modules:
    - ieee7007.Evm: The evm ontology loaded on memory with some useful functions for this ontology
      already present.
    - ieee7007.Nep: The nep ontology loaded on memory with some useful functions for this ontology
      already present.

Usage:
    This module has four main functionalities:
    1) Load individuals and properties over one of the ontological patterns:

    Example 1:

    ``` python
    import ieee7007

    evm = ieee700.Evm()
    evm.load_individuals_from_file('name_of_the_file.csv')

    # If its important to save this ontology for future use, it can be saved in a file
    evm.save_to_file('new_ontology.owl')
    ```


    Where the name_of_the_file.csv has the following format:

    To load an individual: IndividualClass,IndividualName
    To load a property between two individuals: PropertyName,source_individual,target_individual

    Check the files on the ./example_data folder for actual examples.

    Example 2:

    ``` python
    import ieee7007

    evm = ieee700.Evm()
    robot = evm.new_individual(ieee7007.types.IEEE7007Classes.nepRobot, "robot")
    camera = evm.new_individual(ieee7007.types.IEEE7007Classes.evmEthicalBehaviorMonitor, "camera")
    evm.new_property(ieee7007.types.IEEE7007Properties.evmObserves, camera, robot)

    # If its important to save this ontology for future use, it can be saved in a file
    evm.save_to_file('new_ontology.owl')
    ```

    2) Perform the reasoning over the ontology:
    Example:

    ``` python
    import ieee7007

    evm = ieee700.Evm()
    # ... load individuals, etc.
    evm.reasoning() # can also be called passing a boolean to enable verbose reasoning.
    ```

    3) Navigate through an ontology with the navigation functions:
    Example:
    ``` python
    import ieee7007

    evm = ieee700.Evm()
    robot = evm.new_individual(ieee7007.types.IEEE7007Classes.nepRobot, "robot")
    robot2 = evm.new_individual(ieee7007.types.IEEE7007Classes.nepRobot, "robot")
    camera = evm.new_individual(ieee7007.types.IEEE7007Classes.evmEthicalBehaviorMonitor, "camera")
    evm.new_property(ieee7007.types.IEEE7007Properties.evmObserves, camera, robot)

    evm.nav.get_all_properties_relations_of_an_individual(camera)
    # the line above will return the following:
    # [property: .evmobserves, source: evm.camera, target: evm.robot,
    #  property: .evmobserves, source: evm.camera, target: evm.robot2]

    # the following illustrates how to access those information:
    for relation in evm.nav.get_all_properties_relations_of_an_individual(camera):
        if robot == relation.target:
            print("camera has the property {} with the individual 'robot'".format(relation.prop))

        if robot2 == relation.target:
            print("camera also relates({}) with the individual 'robot2'".format(relation.prop))

        else:
            print("I dont know who is the target of the {} property of the
            camera".format(relation.prop))

        # the relation variable has the .prop, the .source and the .target attributes
    ```

    4) Work with the ontology the same way as documented in owlready2 library:
    Example:
    ``` python
    import ieee7007

    evm = ieee700.Evm()
    # load the individuals and properties

    ontology = evm.ontology()

    # ontology is a owlready2 regular ontology object.

    # If the 'world' of the ontology is needed, it can be accessed through:

    world = evm.world()

    # the world is needed in order to call operations such as the reasoning through the owlready2
    # api.
    ```

    ```

Dependencies:
    Owlready2

Version:
    1.0.0

Author:
    Hugo Constantinopolos
"""

# Import necessary modules or functions here

from ieee7007.evm import Evm
from ieee7007 import types
