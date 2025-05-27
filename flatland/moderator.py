from typing import List
from .objects.objects import GameObject, Stone, Animal

class InteractionModerator:
    def resolve(self, objects: List[GameObject], world):
        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if i != j and obj1.x == obj2.x and obj1.y == obj2.y:
                    obj1.interact(obj2, world)
                    obj2.interact(obj1, world)

        for obj in objects:
            if isinstance(obj, Stone) and getattr(obj, "moving", False):
                for other in objects:
                    if other is not obj and obj.x == other.x and obj.y == other.y:
                        if isinstance(other, Animal):
                            print(f"{type(obj).__name__} hit {type(other).__name__}, causing damage!")
                            other.health -= 1
                        obj.moving = False