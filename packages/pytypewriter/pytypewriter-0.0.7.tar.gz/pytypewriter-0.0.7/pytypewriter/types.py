#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 9/20/19
"""
.. currentmodule:: pytypewriter.types
.. moduleauthor:: Pat Daburu <pat@daburu.net>

If you're dealing with Python types, deal here.
"""
import importlib
import sys
from typing import TypeVar
from .errors import PyTypewriterException


class InvalidTypeException(PyTypewriterException):
    """
    Raised when an attempt is made to retrieve an non-existent type from a
    fully-qualified name.

    .. seealso::

        :py:func:`pycls <pycls>`
    """


def pyfqn(obj) -> str:
    """
    Get the fully-qualified name (FQN) of an object's type.

    :param obj: the object
    :return: the fully-qualified type name
    """
    _cls = obj if isinstance(obj, type) else type(obj)
    return f"{_cls.__module__}.{_cls.__name__}"


def pycls(fqn: str) -> TypeVar:
    """
    Get the class to which a fully-qualified name (FQN) refers.

    :param fqn: the fully-qualified name of the class
    :return: the class described by the fully-qualified name (FQN)
    """
    # Split up the fqn (fully-qualified name) at the dots.
    tokens = fqn.split('.')
    # Put the module name back together.
    modname = '.'.join(tokens[:-1])
    # Let's get the module in which
    try:
        mod = sys.modules[modname]
    except KeyError:
        mod = importlib.import_module(modname)
    # The name of the class is the last token.  Retrieve it from the module.
    _cls = getattr(mod, tokens[-1])
    # That's our answer.
    return _cls
