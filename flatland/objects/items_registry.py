from typing import TYPE_CHECKING, Any, Type

from ..logger import Logger

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


class Registry:
    def __init__(self) -> None:
        self._registry: dict[str, "Type[GameObject]"] = dict()
        self.logger = Logger()

    def register(self, cls: type) -> type:
        self.logger.info(f"About to register {cls.__name__}")
        self._registry[cls.__name__] = cls
        return cls

    def create(self, cls_name: str, *args: Any, **kwargs: Any) -> "GameObject":
        """
        This method allows to instantiate a class of given type
        """
        return self._registry[cls_name](*args, **kwargs)

    def list_all(self) -> list[str]:
        return list(self._registry.keys())


registry = Registry()
