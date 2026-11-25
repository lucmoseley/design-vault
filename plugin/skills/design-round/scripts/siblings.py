import importlib.util
import os
import sys


def load(here, file):
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
