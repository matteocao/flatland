"""
This is probably the most fundamental submodule, the one where the object prototypes are defined.

To build a new prototype - that than can be instantiated in the game - one simply needs to combine the
relevant mixins and set the needed attributes, including the location of the animation sprites.

Extended objects need to have children objects that participate in sharing encumbrance and health.

The best approach to learn is to try build new ones, register them to level_0 and test them.

Reading how the exising objects are made is also extremely useful to avoid forgetting some interactions or
characteristics.
"""

from . import base_objects, items, items_2, items_registry
