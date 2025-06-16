import glob
import random
import string
from typing import TYPE_CHECKING

from ..consts import MAX_X, MAX_Y, TILE_SIZE
from ..objects.items_registry import registry
from .build_tile_map import build_tile_map
from .level import Level
from .level_factory import factory

if TYPE_CHECKING:
    from ..objects.items import Ground


@factory.register("level_0")
def build_level_0() -> Level:
    level = Level()
    number = 0
    width, height = 12, 9
    cls_name = "Ground"
    list_of_possible_tiles: list["Ground"] = []
    png_files = glob.glob("assets/sprites/terrain/*.png")
    for tile_name_png in png_files:
        tile_name = tile_name_png[:-4]

        obj: "Ground" = registry.create(  # type: ignore
            cls_name=cls_name, x=0, y=0, name=tile_name, health=10, tile_name=tile_name
        )
        list_of_possible_tiles.append(obj)
    terrain = build_tile_map(list_of_possible_tiles, width, height)
    for i, lst_obj in enumerate(terrain):
        for j, obj in enumerate(lst_obj):
            new_obj = registry.create(  # type: ignore
                cls_name=cls_name,
                x=j,
                y=i,
                name=obj.tile_name,
                health=obj.health,
                tile_name=obj.tile_name,
            )
            level.register(new_obj)

    cow = registry.create(
        cls_name="Cow",
        x=random.randint(0, 10),
        y=random.randint(0, 4),
        name="lola",
        health=5,
        vision_range=5,
        hearing_range=3,
    )
    goblin = registry.create(
        cls_name="Goblin",
        x=random.randint(0, 10),
        y=random.randint(0, 4),
        name="ashpack",
        health=9,
        vision_range=3,
        hearing_range=5,
    )
    stone = registry.create(
        cls_name="Stone",
        x=random.randint(0, 9),
        y=random.randint(0, 4),
        name="a rock",
        health=50,
    )
    cow_shadow = registry.create(
        cls_name="CowShadow",
        x=cow.x,
        y=cow.y,
        name="lola_shadow",
        health=100,
    )
    portal = registry.create(
        cls_name="Portal",
        x=4,
        y=4,
        name="portal",
        health=200,
    )
    robe_torso = registry.create(
        cls_name="RobeTorso",
        x=random.randint(0, 9),
        y=random.randint(0, 4),
        name="robe",
        health=100,
    )
    shoes = registry.create(
        cls_name="Shoes",
        x=random.randint(0, 9),
        y=random.randint(0, 4),
        name="shoes",
        health=100,
    )
    hood = registry.create(
        cls_name="Hood",
        x=random.randint(0, 9),
        y=random.randint(0, 4),
        name="hood",
        health=100,
    )
    skirt = registry.create(
        cls_name="Skirt",
        x=random.randint(0, 9),
        y=random.randint(0, 4),
        name="skirt",
        health=100,
    )
    house = registry.create(
        cls_name="HouseOneMain",
        x=7,
        y=6,
        name="house",
        health=200,
    )
    housepart = registry.create(
        cls_name="HouseOnePartOne",
        x=7,
        y=6,
        name=f"house_img2",
        health=200,
    )
    housepart.parent = house
    level.register(housepart)
    house.children.append(housepart)
    for i in range(3):
        housepart = registry.create(
            cls_name="HouseOnePartTwo",
            x=7,
            y=6,
            name=f"house{i}",
            health=200,
        )
        housepart.parent = house
        level.register(housepart)
        house.children.append(housepart)
    house_door = registry.create(
        cls_name="Door",
        x=4,
        y=4,
        name="door",
        health=200,
    )
    house.children.append(house_door)
    house_door.parent = house
    house_door.level_key = "house_1"  # type: ignore
    house_door.exit_name = "portal"  # type: ignore
    level.register(house_door)
    level.register(house)
    # player stuff
    level.register(robe_torso)
    level.register(shoes)
    level.register(hood)
    level.register(skirt)

    for _ in range(number + 1):
        orangetree = registry.create(
            cls_name="OrangeTreeOne",
            x=random.randint(0, 9),
            y=random.randint(0, 4),
            name="orangetree",
            health=200,
        )
        level.register(orangetree)

    portal.level_key = f"level_{(number+1)%3}"  # type: ignore
    portal.exit_name = "portal"  # type: ignore

    cow_shadow.parent = cow
    cow.children.append(cow_shadow)

    level.register(cow)
    level.register(cow_shadow)

    level.register(stone)
    level.register(goblin)

    level.register(portal)
    return level


@factory.register("level_1")
def build_level_1() -> Level:
    level = Level()
    number = 1
    width, height = 12, 9
    # build terrain

    cls_name = "Ground"
    list_of_possible_tiles: list["Ground"] = []
    png_files = glob.glob("assets/sprites/terrain/*.png")
    for tile_name_png in png_files:
        tile_name = tile_name_png[:-4]

        obj: "Ground" = registry.create(  # type: ignore
            cls_name=cls_name, x=0, y=0, name=tile_name, health=10, tile_name=tile_name
        )
        list_of_possible_tiles.append(obj)
    terrain = build_tile_map(list_of_possible_tiles, width, height)
    for i, lst_obj in enumerate(terrain):
        for j, obj in enumerate(lst_obj):
            new_obj: "Ground" = registry.create(  # type: ignore
                cls_name=cls_name,
                x=j,
                y=i,
                name=obj.tile_name,
                health=obj.health,
                tile_name=obj.tile_name,
            )
            level.register(new_obj)
    cow = registry.create(
        cls_name="Cow",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="lola",
        health=5,
        vision_range=5,
        hearing_range=3,
    )
    goblin = registry.create(
        cls_name="Goblin",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="ashpack",
        health=9,
        vision_range=3,
        hearing_range=5,
    )
    stone = registry.create(
        cls_name="Stone",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="a rock",
        health=50,
    )
    cow_shadow = registry.create(
        cls_name="CowShadow",
        x=cow.x,
        y=cow.y,
        name="lola_shadow",
        health=100,
    )
    portal = registry.create(
        cls_name="Portal",
        x=4,
        y=4,
        name="portal",
        health=200,
    )

    for _ in range(number + 1):
        orangetree = registry.create(
            cls_name="OrangeTreeOne",
            x=random.randint(0, 9),
            y=random.randint(0, 9),
            name="orangetree",
            health=200,
        )
        level.register(orangetree)

    portal.level_key = f"level_{(number+1)%3}"  # type: ignore
    portal.exit_name = "portal"  # type: ignore

    cow_shadow.parent = cow
    cow.children.append(cow_shadow)

    level.register(cow)
    level.register(cow_shadow)

    level.register(stone)
    level.register(goblin)

    level.register(portal)
    return level


@factory.register("level_2")
def build_level_2() -> Level:
    level = Level()
    number = 2
    width, height = 12, 9
    # build terrain

    cls_name = "Ground"
    list_of_possible_tiles: list["Ground"] = []
    png_files = glob.glob("assets/sprites/terrain/*.png")
    for tile_name_png in png_files:
        tile_name = tile_name_png[:-4]

        obj: "Ground" = registry.create(  # type: ignore
            cls_name=cls_name, x=0, y=0, name=tile_name, health=10, tile_name=tile_name
        )
        list_of_possible_tiles.append(obj)
    terrain = build_tile_map(list_of_possible_tiles, width, height)
    for i, lst_obj in enumerate(terrain):
        for j, obj in enumerate(lst_obj):
            new_obj: "Ground" = registry.create(  # type: ignore
                cls_name=cls_name,
                x=j,
                y=i,
                name=obj.tile_name,
                health=obj.health,
                tile_name=obj.tile_name,
            )
            level.register(new_obj)
    cow = registry.create(
        cls_name="Cow",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="lola",
        health=5,
        vision_range=5,
        hearing_range=3,
    )
    goblin = registry.create(
        cls_name="Goblin",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="ashpack",
        health=9,
        vision_range=3,
        hearing_range=5,
    )
    stone = registry.create(
        cls_name="Stone",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="a rock",
        health=50,
    )
    cow_shadow = registry.create(
        cls_name="CowShadow",
        x=cow.x,
        y=cow.y,
        name="lola_shadow",
        health=100,
    )
    portal = registry.create(
        cls_name="Portal",
        x=4,
        y=4,
        name="portal",
        health=200,
    )

    for _ in range(number + 1):
        orangetree = registry.create(
            cls_name="OrangeTreeOne",
            x=random.randint(0, 9),
            y=random.randint(0, 9),
            name="orangetree",
            health=200,
        )
        level.register(orangetree)

    portal.level_key = f"level_{(number+1)%3}"  # type: ignore
    portal.exit_name = "portal"  # type: ignore

    cow_shadow.parent = cow
    cow.children.append(cow_shadow)

    level.register(cow)
    level.register(cow_shadow)

    level.register(stone)
    level.register(goblin)

    level.register(portal)
    return level


@factory.register("house_1")
def build_level_house_1() -> Level:
    level = Level()
    width, height = 3, 3
    # build terrain

    cls_name = "Ground"
    list_of_possible_tiles: list["Ground"] = []
    png_files = glob.glob("assets/sprites/terrain/*.png")
    for tile_name_png in png_files:
        tile_name = tile_name_png[:-4]

        obj: "Ground" = registry.create(  # type: ignore
            cls_name=cls_name, x=0, y=0, name=tile_name, health=10, tile_name=tile_name
        )
        list_of_possible_tiles.append(obj)
    terrain = build_tile_map(list_of_possible_tiles, width, height)
    for i, lst_obj in enumerate(terrain):
        for j, obj in enumerate(lst_obj):
            new_obj: "Ground" = registry.create(  # type: ignore
                cls_name=cls_name,
                x=j,
                y=i,
                name=obj.tile_name,
                health=obj.health,
                tile_name=obj.tile_name,
            )
            level.register(new_obj)
    portal = registry.create(
        cls_name="Portal",
        x=1,
        y=1,
        name="portal",
        health=200,
    )
    portal.level_key = "level_0"  # type: ignore
    portal.exit_name = "door"  # type: ignore

    level.register(portal)
    return level
