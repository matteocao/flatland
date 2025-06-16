from .level import Level
from .level_factory import factory

world = {key: factory.create(key) for key in factory.level_keys()}
