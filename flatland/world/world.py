from .level import Level
from .register_to_level import register_objects, register_terrain

world = {f"level_{i}": register_objects(register_terrain(Level(), 12, 9), i) for i in range(3)}
