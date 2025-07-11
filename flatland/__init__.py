import os
import pathlib

if os.environ.get("VERBOSE_LOGS", None) is None:
    os.environ["VERBOSE_LOGS"] = "false"

if os.environ.get("GITHUB_ACTIONS") == "true":
    os.environ["SDL_AUDIODRIVER"] = "dummy"

from . import (
    __main__,
    actions,
    animations,
    consts,
    game,
    interactions,
    internal,
    llm_stub,
    multiplayer,
    objects,
    sensors,
    world,
)

__doc__ = pathlib.Path(__file__).parent.parent / "README.md"  # type: ignore
__doc__ = __doc__.read_text()  # type: ignore
