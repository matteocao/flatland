import pathlib

from . import __main__, actions, consts, interactions, internal, llm_stub, objects, sensors, world

__doc__ = pathlib.Path(__file__).parent.parent / "README.md"  # type: ignore
__doc__ = __doc__.read_text()  # type: ignore
