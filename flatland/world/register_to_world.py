import random
import string

from ..consts import MAX_X, MAX_Y, TILE_SIZE
from ..objects.items_registry import registry
from .world import world

# Register objects
for (
    cls_name
) in registry.list_all():  # TODO: this will create one instance per object, but this is not general
    rnd_name = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    obj = registry.create(
        cls_name=cls_name,
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name=rnd_name,
        health=random.randint(3, 9),
        vision_range=5,
        hearing_range=3,
        temperature=12.3,
    )
    world.register(obj)
