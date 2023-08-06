"""Registration for keywords, checks, and reporters."""

import inspect
import os
import pkgutil
from functools import partial
from importlib import import_module

from snakeoil import mappings

from . import __title__, checks, reporters, results

try:
    # This is a file written during installation;
    # if it exists, we defer to it. If it doesn't, then we're
    # running from a git checkout or a tarball.
    from . import _const as _defaults
except ImportError:
    _defaults = object()


def _find_modules(module):
    if getattr(module, '__path__', False):
        for _imp, name, _ in pkgutil.walk_packages(module.__path__, module.__name__ + '.'):
            # skip "private" modules
            if name.rsplit('.', 1)[1][0] == '_':
                continue
            try:
                yield import_module(name)
            except ImportError as e:
                raise Exception(f'failed importing {name!r}: {e}')
    else:
        yield module


def _find_classes(module, matching_cls):
    for _name, cls in inspect.getmembers(module):
        if (inspect.isclass(cls) and issubclass(cls, matching_cls)
                and cls.__name__[0] != '_'):
            yield cls


def _find_obj_classes(module_name, matching_cls):
    module = import_module(f'.{module_name}', __title__)

    # skip top-level, base classes
    base_classes = {matching_cls.__name__: matching_cls}
    if os.path.basename(module.__file__) == '__init__.py':
        for cls in _find_classes(module, matching_cls):
            base_classes[cls.__name__] = cls

    classes = {}
    for m in _find_modules(module):
        for cls in _find_classes(m, matching_cls):
            if cls.__name__ in base_classes:
                continue
            if cls.__name__ in classes and classes[cls.__name__] != cls:
                raise Exception(f'object name overlap: {cls} and {classes[cls.__name__]}')
            classes[cls.__name__] = cls

    return classes


def _GET_VALS(attr, func):
    try:
        result = getattr(_defaults, attr)
    except AttributeError:
        result = func()
    return result


try:
    KEYWORDS = mappings.ImmutableDict(_GET_VALS(
        'KEYWORDS', partial(_find_obj_classes, 'checks', results.Result)))
    CHECKS = mappings.ImmutableDict(_GET_VALS(
        'CHECKS', partial(_find_obj_classes, 'checks', checks.Check)))
    REPORTERS = mappings.ImmutableDict(_GET_VALS(
        'REPORTERS', partial(_find_obj_classes, 'reporters', reporters.Reporter)))
except SyntaxError as e:
    raise SyntaxError(f'invalid syntax: {e.filename}, line {e.lineno}')
