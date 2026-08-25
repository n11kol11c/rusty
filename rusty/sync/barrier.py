"""Barrier — blocks until N threads arrive."""
from __future__ import annotations
"""Barrier — thread synchronization barrier.

Provides Barrier for blocking until a specified number of threads
have all arrived at the barrier point.
"""

import threading


class Barrier:
    __slots__ = ("_count", "_threshold", "_lock", "_condition", "_generation")

    def __init__(self, count: int) -> None:
        if count == 0:
            raise ValueError("count cannot be zero")
        self._count = count
        self._threshold = count
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._generation = 0

    def wait(self) -> int:
        with self._condition:
            generation = self._generation
            self._count -= 1
            if self._count == 0:
                self._generation += 1
                self._count = self._threshold
                self._condition.notify_all()
                return 0
            while generation == self._generation:
                self._condition.wait()
            return 1
