"""Cow — copy-on-write, lazily cloned borrowed or owned data."""
from __future__ import annotations
"""Cow — copy-on-write abstraction.

Provides Cow[T] for lazily cloned data that is only copied when mutated.
Can hold either borrowed or owned data.
"""

import copy
from dataclasses import dataclass
from typing import Callable, ClassVar, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True, slots=True)
class Cow(Generic[T]):
    _Borrowed: ClassVar[type]
    _Owned: ClassVar[type]

    def is_borrowed(self) -> bool:
        return isinstance(self, _CowBorrowed)

    def is_owned(self) -> bool:
        return isinstance(self, _CowOwned)

    def as_ref(self) -> T:
        if isinstance(self, _CowBorrowed):
            return self._data
        return self._data

    def into_owned(self) -> T:
        if isinstance(self, _CowOwned):
            return self._data
        return copy.deepcopy(self._data)

    def to_owned(self) -> T:
        if isinstance(self, _CowOwned):
            return self._data
        return copy.deepcopy(self._data)

    def map(self, fn: Callable[[T], U]) -> Cow[U]:
        if isinstance(self, _CowOwned):
            return CowOwned(fn(self._data))
        return CowBorrowed(fn(self._data))

    def unwrap(self) -> T:
        if isinstance(self, _CowOwned):
            return self._data
        return self._data

    def __repr__(self) -> str:
        if isinstance(self, _CowBorrowed):
            return f"Cow::Borrowed({self._data!r})"
        return f"Cow::Owned({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cow):
            return self.as_ref() == other.as_ref()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.as_ref())


@dataclass(frozen=True, slots=True)
class _CowBorrowed(Cow[T]):
    _data: T


@dataclass(frozen=True, slots=True)
class _CowOwned(Cow[T]):
    _data: T


Cow._Borrowed = _CowBorrowed
Cow._Owned = _CowOwned


def CowBorrowed(value: T) -> Cow[T]:
    return _CowBorrowed(value)


def CowOwned(value: T) -> Cow[T]:
    return _CowOwned(value)
