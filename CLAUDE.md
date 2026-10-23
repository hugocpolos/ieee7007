# ieee7007

Python library over Owlready2 for the IEEE 7007-2021 ontologies (ERAS). Bundles the machine-
readable `evm.owl` → `nep.owl` → `tlo.owl` in `ieee7007/ontologies/`. Used by
`nav2-to-onto-compiler`, `nav2-to-onto-runtime`, and earlier by the CNCS2 and RCSM projects.

Project knowledge for nav2-to-onto lives in `../nav2-to-onto-vault`. This file holds only
timeless, implementation-specific facts about this library.

## API

- `IEEE7007Base` / `Evm` (`ieee7007base.py`, `evm.py`) — load the Owlready2 world and ontology;
  save; run HermiT (`sync_reasoner_hermit`).
- `Factory` (`factory.py`) — maps `IEEE7007Classes` to Owlready2 classes.
- `IndividualsLoader` (`instances_loader.py`) — create individuals/relations from code or CSV.
- `OntologyNavigator` (`navigator.py`) — query relations.
- `types.py` — `IEEE7007Classes`, `IEEE7007Properties` enums: the single source of truth for
  which classes/properties exist. Consumers must not bypass them.

## Rules

- Only expose classes/properties that exist in the bundled `.owl` files.
- Changing the bundled `.owl` files is a breaking change: bump the version.
- Must not depend on ROS.

## Build / test

`pip install -e .` ; tests in `tests/` (pytest). Packaging is legacy `setup.py`.

Plotting (`OntologyNavigator.plot*`) is an optional extra: `pip install -e .[plot]` (networkx,
matplotlib, pygraphviz — the last needs the system graphviz headers, `libgraphviz-dev`). Plot
imports are lazy, so the core library depends only on owlready2; plot tests skip without the extra.
