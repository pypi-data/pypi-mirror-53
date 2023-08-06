# -*- coding: utf-8 -*-

"""Top-level package for @model."""

__author__ = """Alexandr Mansurov"""
__email__ = 'alex@eghuro.cz'
__version__ = '0.1.0'


def add_dynamo(klass, param):
    name = '__' + param
    def innerdynamo(self):
        return self.__dict__[name]
    innerdynamo.__name__ = param
    setattr(klass, innerdynamo.__name__, innerdynamo)


def model(*params, **mkw):
    def model_decorator(klass):
        optional = mkw.pop('optional', [])
        old_init = klass.__init__

        def new_init(self, *args, **kwargs):
            kws = dict()
            for param in params:
                kws[param] = kwargs[param]
                del kwargs[param]

            for param in optional:
                x = kwargs.pop(param, None)
                kws[param] = x

            old_init(self, *args, **kwargs)

            for param in list(params) + optional:
                add_dynamo(klass, param)
                name = '__' + param
                setattr(self, name, kws[param])

        klass.__init__ = new_init
        return klass
    return model_decorator
