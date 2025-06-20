"""
This submodule handles the Level and world objects.

These are aggregators of objects and the places where levels are built and registered to the world.

To build a level, simply configure its yaml file. Do not forget to connect parents and children when needed,
for example the Cow with its CowShadow.
"""

from . import build_tile_map, level, level_factory, register_to_level, world
