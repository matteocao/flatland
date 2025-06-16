"""
This is the factory pattern to generate levels.
Each level shall be built and registered in the factory
"""

# level_factory.py

from typing import Any, Callable

from .level import Level

# The builder functions you will register: always return a Level
LevelBuilder = Callable[..., Level]


class LevelFactory:
    """Factory specialized for builder functions that create Levels."""

    def __init__(self) -> None:
        self._registry: dict[str, LevelBuilder] = {}

    def register(self, key: str) -> Callable[[LevelBuilder], LevelBuilder]:
        """Decorator to register a builder function."""

        def _decorator(builder: LevelBuilder) -> LevelBuilder:
            if key in self._registry:
                raise KeyError(f"Level '{key}' is already registered.")
            self._registry[key] = builder
            return builder

        return _decorator

    def level_keys(self) -> set[str]:
        return set(self._registry.keys())

    def create(self, key: str, **kwargs: Any) -> Level:
        """Create a Level by calling the registered builder function."""
        if key not in self._registry:
            raise ValueError(f"No level registered under key '{key}'.")
        builder = self._registry[key]
        return builder(**kwargs)


# A global factory instance
factory = LevelFactory()
