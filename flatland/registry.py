from collections import defaultdict

class Registry:
    def __init__(self):
        self._registry = defaultdict(dict)

    def register(self, category: str):
        def wrapper(cls):
            self._registry[category][cls.__name__] = cls
            return cls
        return wrapper

    def auto_register(self, category: str):
        def decorator(cls):
            self._registry[category][cls.__name__] = cls
            return cls
        return decorator

    def create(self, category: str, name: str, *args, **kwargs):
        return self._registry[category][name](*args, **kwargs)

    def list_all(self, category: str):
        return list(self._registry[category].keys())

registry = Registry()