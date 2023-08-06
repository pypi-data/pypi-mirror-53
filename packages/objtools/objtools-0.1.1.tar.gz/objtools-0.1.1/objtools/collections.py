"""
This module provides helpers for working with collections (as in abstract
base classes defined in the ``collections.abc`` standard Python module:
iterables, iterators, mappings, etc.).
"""
from typing import Mapping, Dict, Sequence, Set, Iterable, ByteString, Any


def namespacify(value: Any) -> Any:
    """
    Turn all mappings into :class:`Namespace` instances as needed.

    :param value: Anything that may be a mapping or may be an iterable
       that may hold a mapping.
    :returns:
       * The value itself, if it is a Namespace instance or is neither
         a mapping, a sequence, a set, or an iterable;
       * A :class:`Namespace` instance for a mapping;
       * A list holding the result of calling :meth:`namespacify` on
         every item for a sequence;
       * A set holding the result of calling :meth:`namespacify` on
         every item for a set;
       * A ``map`` object applying :meth:`namespacify` on every item
         for other iterables.
    """
    if isinstance(value, Namespace):
        return value
    if isinstance(value, Mapping):
        return Namespace(value)
    if isinstance(value, (str, ByteString)):
        # Do not treat strings and bytestrings as normal sequences
        return value
    if isinstance(value, Sequence):
        return list(map(namespacify, value))
    if isinstance(value, Set):
        return set(map(namespacify, value))
    if isinstance(value, Iterable):
        return map(namespacify, value)
    return value


class Namespace(Dict):
    """
    A subclass of ``dict`` which allows accessing items using attributes.
    Attributes and items are kept in sync; deleting an item deletes the
    attribute, and updating an item updates the attribute, and vice-versa.

    Getting an attribute will call :meth:`namespacify` on the returned value,
    to allow easier manipulation of complex structures such as JSON documents:

    .. code:: python

       >>> from objtools.collections import Namespace
       >>> ns = Namespace({'foo': [{'bar': {'baz': 42}}]})
       >>> ns.foo[0].bar.baz
       42
    """

    def __getitem__(self, name: Any) -> Any:
        return namespacify(super().__getitem__(name))

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(repr(name))

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        try:
            del self[name]
        except KeyError as e:
            raise AttributeError(str(e))

    def __repr__(self) -> str:
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    def __str__(self) -> str:
        return str(dict(self))

    def _repr_pretty_(self, p: Any, cycle: bool) -> None:
        # IPython's pretty printing
        if cycle:
            p.text('{}(...)'.format(self.__class__.__name__))
        else:
            p.text('{}('.format(self.__class__.__name__))
            p.pretty(dict(self))
            p.text(')')

    def copy(self) -> 'Namespace':
        """
        Create a shallow copy of this namespace.
        """
        return self.__class__(self)
