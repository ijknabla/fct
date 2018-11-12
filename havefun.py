
__all__ = [
    "curried_map",
    "curried_filter",
    "ComposableCall",
]

def doNothing(arg : object) -> object:
    return arg

from collections.abc import Callable

class ComposableCall(Callable):
    
    def __init__(self, callable=None):
        if callable is None:
            callable = doNothing
        self._callable = callable

    def copy(self):
        return self.__class__(self._callable)
     
    def before(self, other):
        def composed(*args):
            return other(self(*args))
        return self.__class__(composed)

    def __call__(self, *args):
        return self._callable(*args)
    
    def after(self, other):
        def composed(*args):
            return self(other(*args))
        return self.__class__(composed)

    __rshift__ = before
    __lshift__ = after

    __rrshift__ = __lshift__
    __rlshift__ = __rshift__

@ComposableCall
def apply(x):
    @ComposableCall
    def _apply(func):
        return func(x)
    return _apply

from functools import partial
@ComposableCall
def curried_map(func):
    return ComposableCall(partial(map, func))

@ComposableCall
def curried_filter(func=None):
    return ComposableCall(partial(filter, func))
