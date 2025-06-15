from .level import Level
from .level_factory import factory

world = {f"level_{i}": factory.create(f"level_{i}") for i in range(3)}
