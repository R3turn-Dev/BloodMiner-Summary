import importlib

__all__ = ["root", "api"]

blueprints = []
for name in __all__:
    blueprints.append(importlib.import_module("pages."+name))