from functools import partial
from importlib import import_module


try:
    from pygments import highlight, lexers, formatters
except:
    highlight_json = lambda x: x
else:
    highlight_json = partial(highlight, lexer=lexers.JsonLexer(), formatter=formatters.TerminalFormatter())


def import_object(path):
    module_name, obj_name = path.split(":")
    return getattr(import_module(module_name), obj_name)
