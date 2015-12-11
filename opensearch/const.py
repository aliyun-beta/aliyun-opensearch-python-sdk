# coding=utf-8
import sys


class _const:

    class ConstError(TypeError):
        pass

    class ArgError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const instance attribute (%s)" % name)
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError("Can't unbind const const instance attribute (%s)" % name)
        raise AttributeError("const instance has no attribute '%s'" % name)


sys.modules[__name__] = _const()
