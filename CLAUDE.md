# ieee7007

Python library over Owlready2 for the IEEE 7007-2021 ontologies (ERAS). Bundles the machine-
readable `evm.owl` → `nep.owl` → `tlo.owl` in `ieee7007/ontologies/`. Used by
`nav2-to-onto-compiler`, `nav2-to-onto-runtime`, and earlier by the CNCS2 and RCSM projects.

Project knowledge for nav2-to-onto lives in `../nav2-to-onto-vault`. This file holds only
timeless, implementation-specific facts about this library.

## API

- `IEEE7007Base` / `Evm` (`ieee7007base.py`, `evm.py`) — load the Owlready2 world and ontology;
  save; run HermiT (`sync_reasoner_hermit`). `ontology()` is the *individuals ontology* (where
  `new_individual` creates and what `save_to_file` writes); `schema()` is the bundled ontology.
- `Factory` (`factory.py`) — looks up Owlready2 classes by local name (current or pre-0.3.0).
- `IndividualsLoader` (`instances_loader.py`) — create individuals/relations from code or CSV.
- `OntologyNavigator` (`navigator.py`) — query relations.
- `types.py` — `IEEE7007Classes`, `IEEE7007Properties` enums: the single source of truth for
  which classes/properties exist. Consumers must not bypass them.

## IRIs

- Every term is `https://w3id.org/ieee7007/{tlo,nep,evm}#<name>`, e.g. `…/nep#nepAgentPlan`;
  ontology IRIs are `https://w3id.org/ieee7007/{tlo,nep,evm}`, with `owl:versionIRI`
  `https://w3id.org/ieee7007/<version>/<name>`. `NAMESPACE` and `ontology_iri()` in
  `ieee7007base.py` hold them.
- Local names carry no ontology prefix (`nep#Robot`, `nep#applies`, `tlo#affects`), except the 7
  that would otherwise clash: `tloAgent`/`nepAgent`, `tloSituation`/`nepSituation`,
  `tloEnumDataTypes`/`nepEnumDataTypes`/`evmEnumDataTypes`. Local names are unique across the
  three ontologies (Owlready2 and `Factory` look terms up by local name; `tests/test_names.py`).
- `IEEE7007Classes`/`IEEE7007Properties` *member names* keep the prefix (`nepRobot`,
  `nepApplies`); their *values* are the local names. `factory.resolve_name` also accepts the
  pre-0.3.0 prefixed names (`nepRobot`, `nepapplies`), so old CSV files still load.
- The bundled files are loaded under those IRIs from the package copies (`load(fileobj=…)`, in
  import order: TLO, NEP, EVM), so `owl:imports` never triggers a download and nothing depends on
  the install path.
- Individuals live in their own ontology (`Evm(individuals_iri=…)`, default a `urn:uuid:` IRI),
  which imports EVM by IRI. `save_to_file` writes only that ontology (N-Triples) and must never
  contain a filesystem path; `Evm(individuals_file=…)` loads such a file back, and
  `import_individuals_file()` adds another saved file as a read-only import. A saved file that
  imports another individuals ontology can only be reloaded after that one is loaded.

## Rules

- Only expose classes/properties that exist in the bundled `.owl` files.
- Changing the bundled `.owl` files is a breaking change: bump the version. On every version
  bump, also update the three `owl:versionIRI`s.
- Never put `file://` or relative IRIs back into the `.owl` files (`tests/test_iris.py` checks).
- Must not depend on ROS.

## Build / test

Packaging is `pyproject.toml` (setuptools backend); the version lives there. The `.owl` files ship
as package data. `pip install -e ".[test]"` ; tests in `tests/` (`pytest`). `requirements.txt` pins
the owlready2 version CI and the pipenv environment use.

Plotting (`OntologyNavigator.plot*`) is an optional extra: `pip install -e ".[plot]"` (networkx,
matplotlib, pygraphviz — the last needs the system graphviz headers, `libgraphviz-dev`). Plot
imports are lazy, so the core library depends only on owlready2; plot tests skip without the extra.
