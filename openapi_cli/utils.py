from importlib import import_module


def import_object(path):
    module_name, obj_name = path.split(":")
    return getattr(import_module(module_name), obj_name)
