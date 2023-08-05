import importlib
_USE_CUPY = False


def cuda(flag):
    global _USE_CUPY
    _USE_CUPY = flag


def use_cuda():
    global _USE_CUPY
    return _USE_CUPY


def xp_factory():
    if use_cuda():
        return importlib.import_module('cupy')
    else:
        return importlib.import_module('numpy')
