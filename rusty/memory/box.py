"""Box — a heap-allocated value with automatic cleanup."""
from __future__ import annotations
"""Box — a heap-allocated value.

Provides Box[T] for owning a value on the heap with automatic cleanup.
Supports new, from_fn, into_inner, as_ref, as_mut, leak, pin.
"""

from typing import Any, Callable, Generic, TypeVar

from .pin import Pin

T = TypeVar("T")


class Box(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    @classmethod
    def new(cls, value: T) -> Box[T]:
        return cls(value)

    @classmethod
    def from_fn(cls, fn: Callable[[], T]) -> Box[T]:
        return cls(fn())

    def into_inner(self) -> T:
        return self._value

    def as_ref(self) -> T:
        return self._value

    def as_mut(self) -> T:
        return self._value

    def leak(self) -> T:
        return self._value

    def pin(self) -> Pin[T]:
        return Pin(self._value)

    def __enter__(self) -> Box[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __repr__(self) -> str:
        return f"Box({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Box):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return True

    def __del__(self) -> None:
        self._value = None
