from .level import Level
from .level_factory import factory
from .register_to_level import load_levels_from_yaml

load_levels_from_yaml("assets/levels")

world = {key: factory.create(key) for key in factory.level_keys()}
