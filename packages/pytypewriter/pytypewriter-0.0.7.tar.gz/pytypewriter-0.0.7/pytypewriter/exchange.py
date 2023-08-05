#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 9/21/19
"""
.. currentmodule:: pytypewriter.exchange
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Document exchange... data exchange... it all starts here!
"""
from abc import ABC, abstractmethod
from typing import Any, Mapping
from .types import pycls, pyfqn, InvalidTypeException


class Exportable(ABC):
    """
    Objects that can be exported as and loaded from simple data types
    should extend `Exportable` to make their intentions clear and their
    methods consistent.
    """
    @abstractmethod
    def export(self) -> Mapping[str, Any]:
        """
        Export the instance as a mapping of simple types.

        :return: the mapping
        """

    @classmethod
    @abstractmethod
    def load(cls, data: Mapping[str, Any]) -> Any:
        """
        Create an instance from a mapping.

        :param data: the data
        :return: the instance
        """


def export(exportable: Exportable) -> Mapping[str, Any]:
    """
    Export an :py:class:`Exportable` including meta-data.

    :param exportable: the exportable
    :return: the mapping

    .. note::

        This function will add a ``__type__`` key containing the fully-qualified
        type name.

    .. seealso::

        * :py:func:`load`
        * :py:func:`pyfqn <pytypewriter.types.pyfqn>`
    """
    exported = exportable.export()
    # Add meta-information to the exported data.
    exported['__type__'] = pyfqn(exportable)
    return exported


def load(data: Mapping[str, Any]) -> Any:
    """

    :param data: a mapping that represents the type
    :return: the type instance

    .. note::

        The mapping must contain a ``__type__`` key that contains the
        fully-qualified type name.

    .. seealso::

        * :py:func:`export`
        * :py:func:`pycls <pytypewriter.types.pycls>`
    """
    # Try to get the python class.
    try:
        cls = pycls(data['__type__'])
    except KeyError:
        # If there is no type information, we can't continue.
        raise InvalidTypeException(
            "The data is missing the '__type__' key."
        )
    # Remove meta-information from the data.
    _data = {
        k: v for k, v in data.items()
        if k not in ('__type__',)
    }
    # Let the class take if from here.
    return cls.load(_data)
