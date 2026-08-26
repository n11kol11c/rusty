"""Semaphore — counting semaphore for concurrency limiting."""
from __future__ import annotations
"""Semaphore — counting semaphore.

Provides Semaphore for limiting concurrent access to a resource
with acquire, release, and context manager support.
"""

import threading
from typing import Any


class Semaphore:
    __slots__ = ("_semaphore", "_max")

    def __init__(self, max_permits: int) -> None:
        if max_permits <= 0:
            raise ValueError("max_permits must be positive")
        self._semaphore = threading.Semaphore(max_permits)
        self._max = max_permits

    @classmethod
    def new(cls, max_permits: int) -> Semaphore:
        return cls(max_permits)

    def acquire(self, blocking: bool = True, timeout: float | None = None) -> bool:
        return self._semaphore.acquire(blocking=blocking, timeout=timeout)

    def release(self) -> None:
        self._semaphore.release()

    def available(self) -> int:
        return self._semaphore._value  # type: ignore

    @property
    def max_permits(self) -> int:
        return self._max

    def __enter__(self) -> Semaphore:
        self.acquire()
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"Semaphore(max={self._max})"
