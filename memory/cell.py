"""Cell — interior mutability for Copy types without references."""
from __future__ import annotations
"""Cell — interior mutability for Copy types.

Provides Cell[T] for single-threaded interior mutability without
requiring references. Works with Copy types only.
"""

import copy
from typing import Generic, TypeVar

T = TypeVar("T")


class Cell(Generic[T]):
    __slots__ = ("_value", "_copy")

    def __init__(self, value: T, *, deep: bool = False) -> None:
        self._value = value
        self._copy = deep

    @classmethod
    def new(cls, value: T) -> Cell[T]:
        return cls(value)

    def get(self) -> T:
        if self._copy:
            return copy.deepcopy(self._value)
        return self._value

    def set(self, value: T) -> None:
        self._value = value

    def replace(self, value: T) -> T:
        old = self._value
        self._value = value
        return old

    def swap(self, other: Cell[T]) -> None:
        self._value, other._value = other._value, self._value

    def take(self) -> T:
        old = self._value
        self._value = None  # type: ignore[assignment]
        return old

    def into_inner(self) -> T:
        return self._value

    def as_ptr(self) -> int:
        return id(self._value)

    def __repr__(self) -> str:
        return f"Cell({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return bool(self._value)
