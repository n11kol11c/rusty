"""OnceCell — a cell that can be initialized exactly once."""
from __future__ import annotations
"""OnceCell — a cell which can be written to only once.

Provides OnceCell[T] for lazy one-time initialization of a value.
"""

from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class OnceCell(Generic[T]):
    __slots__ = ("_value", "_initialized")

    def __init__(self) -> None:
        self._value: T = None  # type: ignore[assignment]
        self._initialized = False

    @classmethod
    def new(cls) -> OnceCell[T]:
        return cls()

    @classmethod
    def with_value(cls, value: T) -> OnceCell[T]:
        cell = cls()
        cell._value = value
        cell._initialized = True
        return cell

    def get(self) -> T | None:
        if not self._initialized:
            return None
        return self._value

    def set(self, value: T) -> bool:
        if self._initialized:
            return False
        self._value = value
        self._initialized = True
        return True

    def get_or_init(self, fn: Callable[[], T]) -> T:
        if self._initialized:
            return self._value
        self._value = fn()
        self._initialized = True
        return self._value

    def try_into_inner(self) -> T | None:
        if not self._initialized:
            return None
        return self._value

    def is_initialized(self) -> bool:
        return self._initialized

    def __repr__(self) -> str:
        if self._initialized:
            return f"OnceCell({self._value!r})"
        return "OnceCell(<uninitialized>)"

    def __bool__(self) -> bool:
        return self._initialized

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OnceCell):
            if not self._initialized or not other._initialized:
                return False
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        if self._initialized:
            return hash(self._value)
        return hash(None)
