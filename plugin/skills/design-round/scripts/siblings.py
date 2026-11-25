"""siblings.py — loads a design-round script beside the caller once per
process, so every caller shares one module and one copy of each error class
(#558). A script imports it by name after putting its own folder on the path:

    HERE = os.path.dirname(os.path.abspath(__file__))
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import siblings  # noqa: E402

    flow = siblings.load(HERE, "check-flow.py")

A module is cached in sys.modules under its file's real path before it runs,
as importlib's own imports are, so a circular load gets the module part-built
rather than a second copy. A script run as the program is that file's module.
"""

import importlib.util
import os
import sys


def load(here, file):
    """The module in `file` in the folder `here`, run on its first load only."""
    path = os.path.realpath(os.path.join(here, file))
    module = sys.modules.get(path)
    if module is not None:
        return module
    main = sys.modules.get("__main__")
    main_file = getattr(main, "__file__", None)
    if main_file and os.path.realpath(main_file) == path:
        return main
    spec = importlib.util.spec_from_file_location(path, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        del sys.modules[path]
        raise
    return module
