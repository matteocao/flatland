from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


@dataclass
class ObjectRepresentation:
    dx: Optional[int] = None
    dy: Optional[int] = None
    noise_intensity: Optional[float] = None
    attractiveness: Optional[float] = None
    visible_size: Optional[float] = None
    source_object: Optional["GameObject"] = None
