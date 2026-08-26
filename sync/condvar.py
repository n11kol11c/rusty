"""Condvar — condition variable for thread coordination."""
from __future__ import annotations
"""Condvar — condition variable.

Provides Condvar for waiting on conditions across threads,
with wait, wait_while, notify_one, and notify_all.
"""

import threading
from typing import Any, Callable


class Condvar:
    __slots__ = ("_condition", "_notify_all")

    def __init__(self, notify_all: bool = True) -> None:
        self._condition = threading.Condition()
        self._notify_all = notify_all

    @classmethod
    def new(cls) -> Condvar:
        return cls()

    def wait(self, lock: threading.Lock | None = None) -> None:
        with self._condition:
            if lock:
                lock.release()
            self._condition.wait()
            if lock:
                lock.acquire()

    def wait_while(self, predicate: Callable[[], bool], lock: threading.Lock | None = None) -> None:
        with self._condition:
            while predicate():
                if lock:
                    lock.release()
                self._condition.wait()
                if lock:
                    lock.acquire()

    def notify_one(self) -> None:
        with self._condition:
            self._condition.notify()

    def notify_all(self) -> None:
        with self._condition:
            self._condition.notify_all()

    def __enter__(self) -> Condvar:
        self._condition.acquire()
        return self

    def __exit__(self, *_: Any) -> None:
        self._condition.release()
