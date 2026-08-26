"""Lazy — deferred computation, evaluated on first access."""
from __future__ import annotations
"""Lazy — deferred computation.

Provides Lazy[T] for lazily computing a value on first access.
"""

import threading
from typing import Callable, Generic, Iterator, TypeVar

T = TypeVar("T")


class Lazy(Generic[T]):
    __slots__ = ("_fn", "_value", "_computed", "_lock")

    def __init__(self, fn: Callable[[], T]) -> None:
        self._fn = fn
        self._value: T = None  # type: ignore[assignment]
        self._computed = False
        self._lock = threading.Lock()

    def force(self) -> T:
        if self._computed:
            return self._value
        with self._lock:
            if not self._computed:
                self._value = self._fn()
                self._computed = True
        return self._value

    def is_forced(self) -> bool:
        return self._computed

    def try_into_inner(self) -> T | None:
        if not self._computed:
            return None
        return self._value

    def __repr__(self) -> str:
        if self._computed:
            return f"Lazy({self._value!r})"
        return "Lazy(<not initialized>)"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Lazy):
            return self.force() == other.force()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.force())

    def __bool__(self) -> bool:
        return bool(self.force())

    def __iter__(self) -> Iterator[T]:
        return iter(self.force())
