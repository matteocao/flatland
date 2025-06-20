import glob
import os
import random
import string
from pathlib import Path
from typing import TYPE_CHECKING

import yaml  # type: ignore

from ..consts import MAX_X, MAX_Y, TILE_SIZE
from ..objects.items_registry import registry
from .build_tile_map import build_tile_map
from .level import Level
from .level_factory import factory

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject
    from ..objects.items import Ground


def load_levels_from_yaml(level_folder: str):
    level_files = Path(level_folder).glob("*.yaml")
    for file_path in level_files:
        with open(file_path, "r") as f:
            level_data = yaml.safe_load(f)
            build_level_from_config(level_data)


def build_level_from_config(config: dict):
    # Register level to factory
    level_key = config["level_key"]
    level = Level(level_key)
    name_to_object = {}

    # First pass: create all objects
    for obj_conf in config["objects"]:
        cls_name = obj_conf["cls_name"]
        x = obj_conf.get("x", 0)
        y = obj_conf.get("y", 0)
        name = obj_conf["name"]
        health = obj_conf.get("health", 10)
        tile_name = obj_conf.get("tile_name")
        other = obj_conf.get("other_attributes", {})
        vision_range = obj_conf.get("vision_range")
        hearing_range = obj_conf.get("hearing_range")

        # Build kwargs
        kwargs = {
            "cls_name": cls_name,
            "x": x,
            "y": y,
            "name": name,
            "health": health,
            "vision_range": vision_range,
            "hearing_range": hearing_range,
            "tile_name": tile_name,
        }

        obj = registry.create(**kwargs)
        for k, v in other.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        name_to_object[name] = obj
        level.register(obj)

    # Second pass: assign parents and children
    for obj_conf in config["objects"]:
        name = obj_conf["name"]
        obj = name_to_object[name]

        parent_name = obj_conf.get("parent")
        if parent_name:
            parent_obj = name_to_object[parent_name]
            obj.parent = parent_obj
            parent_obj.children.append(obj)

        children_names = obj_conf.get("children", [])
        for child_name in children_names:
            child_obj = name_to_object[child_name]
            obj.children.append(child_obj)
            child_obj.parent = obj

    @factory.register(level_key)
    def _level_fn() -> Level:
        return level
