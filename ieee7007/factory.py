"""
Maps class names to the ontology's classes, so individuals can be created by name.
"""

# Ontology prefixes that older versions of this library (and the standard's own NEP/EVM files)
# put at the start of every local name, e.g. 'nepRobot'. Since 0.3.0 the prefix is only in the
# namespace ('https://w3id.org/ieee7007/nep#Robot'), except where dropping it would make two
# terms share a name (nepAgent/tloAgent, nepSituation/tloSituation, *EnumDataTypes).
LEGACY_PREFIXES = ("tlo", "nep", "evm")


def resolve_name(name, names):
    """
    Returns the current local name for `name`, or None.

    Accepts the current local name ('Robot', 'applies') and the prefixed name used before 0.3.0
    ('nepRobot', 'nepapplies').

    Parameters:
        name (str): The name to resolve.
        names: The current local names (anything supporting `in`).
    """
    if name in names:
        return name
    for prefix in LEGACY_PREFIXES:
        if name.startswith(prefix) and name[len(prefix):] in names:
            return name[len(prefix):]
    return None


class Factory:
    """
    Looks up the ontology's classes by local name.
    """

    def __init__(self, ontology):
        self._classes = {cls.name: cls for cls in ontology.world.classes()}

    def get_factory_by_name(self, name):
        """
        Returns the class whose local name is `name` (current or pre-0.3.0 prefixed form),
        or None. Calling the returned class with an individual name creates the individual.
        """
        resolved = resolve_name(name, self._classes)
        return None if resolved is None else self._classes[resolved]
