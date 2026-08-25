"""Rc and Weak — single-threaded reference-counted shared ownership."""
from __future__ import annotations
"""Rc and Weak — reference-counted shared ownership.

Provides Rc[T] for single-threaded reference counting and Weak[T]
for non-owning weak references to break cycles.
"""

from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Rc(Generic[T]):
    __slots__ = ("_value", "_ref_count", "_weak_count")

    def __init__(self, value: T) -> None:
        self._value = value
        self._ref_count = 1
        self._weak_count = 0

    @classmethod
    def new(cls, value: T) -> Rc[T]:
        return cls(value)

    def clone(self) -> Rc[T]:
        self._ref_count += 1
        return Rc._from_raw(self._value, self._ref_count, self._weak_count)

    @classmethod
    def _from_raw(cls, value: T, ref_count: int, weak_count: int) -> Rc[T]:
        rc = cls.__new__(cls)
        rc._value = value
        rc._ref_count = ref_count
        rc._weak_count = weak_count
        return rc

    def downgrade(self) -> Weak[T]:
        self._weak_count += 1
        return Weak._from_raw(self._value, self._ref_count, self._weak_count)

    def strong_count(self) -> int:
        return self._ref_count

    def weak_count(self) -> int:
        return self._weak_count

    def try_unwrap(self) -> T | None:
        if self._ref_count == 1:
            return self._value
        return None

    def as_ptr(self) -> int:
        return id(self._value)

    def into_inner(self) -> T:
        return self._value

    def __enter__(self) -> Rc[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __del__(self) -> None:
        self._ref_count -= 1

    def __repr__(self) -> str:
        return f"Rc({self._value!r}, strong={self._ref_count}, weak={self._weak_count})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Rc):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return True


class Weak(Generic[T]):
    __slots__ = ("_value", "_ref_count", "_weak_count")

    def __init__(self, value: T) -> None:
        self._value = value
        self._ref_count = 0
        self._weak_count = 1

    @classmethod
    def _from_raw(cls, value: T, ref_count: int, weak_count: int) -> Weak[T]:
        w = cls.__new__(cls)
        w._value = value
        w._ref_count = ref_count
        w._weak_count = weak_count
        return w

    def upgrade(self) -> Rc[T] | None:
        if self._ref_count > 0:
            self._ref_count += 1
            return Rc._from_raw(self._value, self._ref_count, self._weak_count)
        return None

    def strong_count(self) -> int:
        return self._ref_count

    def weak_count(self) -> int:
        return self._weak_count

    def as_ptr(self) -> int:
        return id(self._value)

    def is_alive(self) -> bool:
        return self._ref_count > 0

    def __repr__(self) -> str:
        return f"Weak(strong={self._ref_count}, weak={self._weak_count})"

    def __bool__(self) -> bool:
        return self._ref_count > 0

    def __del__(self) -> None:
        self._weak_count -= 1
