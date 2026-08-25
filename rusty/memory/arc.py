"""Arc — thread-safe reference-counted shared ownership."""
from __future__ import annotations
"""Arc — atomic reference-counted shared ownership.

Provides Arc[T] for thread-safe reference counting across multiple threads.
"""

import threading
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Arc(Generic[T]):
    __slots__ = ("_inner", "_ref_count", "_lock")

    def __init__(self, value: T) -> None:
        self._inner = value
        self._ref_count = 1
        self._lock = threading.Lock()

    @classmethod
    def new(cls, value: T) -> Arc[T]:
        return cls(value)

    def clone(self) -> Arc[T]:
        with self._lock:
            self._ref_count += 1
        return Arc._from_raw(self._inner, self._ref_count, self._lock)

    @classmethod
    def _from_raw(cls, value: T, ref_count: int, lock: threading.Lock) -> Arc[T]:
        arc = cls.__new__(cls)
        arc._inner = value
        arc._ref_count = ref_count
        arc._lock = lock
        return arc

    def strong_count(self) -> int:
        with self._lock:
            return self._ref_count

    def try_unwrap(self) -> T | None:
        with self._lock:
            if self._ref_count == 1:
                return self._inner
        return None

    def as_ptr(self) -> int:
        return id(self._inner)

    def into_inner(self) -> T:
        return self._inner

    def make_mut(self) -> T:
        return self._inner

    def __enter__(self) -> Arc[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __del__(self) -> None:
        with self._lock:
            self._ref_count -= 1

    def __repr__(self) -> str:
        return f"Arc({self._inner!r}, strong={self._ref_count})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Arc):
            return self._inner == other._inner
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._inner)

    def __bool__(self) -> bool:
        return True
