"""Mutex — mutual exclusion lock with MutexGuard."""
from __future__ import annotations
"""Mutex — mutual exclusion lock.

Provides Mutex[T] with MutexGuard for protecting shared data across threads.
Supports lock, try_lock, and context manager protocols.
"""

import threading
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class MutexPoisoned(Exception):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("mutex is poisoned")


class MutexLock:
    __slots__ = ("_mutex", "_guard")

    def __init__(self, mutex: Mutex) -> None:
        self._mutex = mutex
        self._guard = None

    def __enter__(self) -> Any:
        self._guard = self._mutex.lock()
        return self._guard

    def __exit__(self, *_: Any) -> None:
        if self._guard is not None:
            self._guard.release()
            self._guard = None


class MutexGuard:
    __slots__ = ("_mutex",)

    def __init__(self, mutex: Mutex) -> None:
        self._mutex = mutex

    @property
    def value(self) -> Any:
        return self._mutex._value

    @value.setter
    def value(self, v: Any) -> None:
        self._mutex._value = v

    def replace(self, v: Any) -> Any:
        old = self._mutex._value
        self._mutex._value = v
        return old

    def swap(self, other: Mutex) -> None:
        self._mutex._value, other._value = other._value, self._mutex._value

    def into_inner(self) -> Any:
        return self._mutex._value

    def release(self) -> None:
        self._mutex._lock.release()

    def __repr__(self) -> str:
        return f"MutexGuard({self._mutex._value!r})"


class Mutex(Generic[T]):
    __slots__ = ("_value", "_lock", "_poisoned")

    def __init__(self, value: T) -> None:
        self._value = value
        self._lock = threading.Lock()
        self._poisoned = False

    @classmethod
    def new(cls, value: T) -> Mutex[T]:
        return cls(value)

    def lock(self) -> MutexGuard:
        if self._poisoned:
            raise MutexPoisoned()
        self._lock.acquire()
        return MutexGuard(self)

    def try_lock(self) -> MutexGuard | None:
        if self._poisoned:
            raise MutexPoisoned()
        acquired = self._lock.acquire(blocking=False)
        if acquired:
            return MutexGuard(self)
        return None

    def into_inner(self) -> T:
        return self._value

    def is_poisoned(self) -> bool:
        return self._poisoned

    def poison(self) -> None:
        self._poisoned = True

    def clear_poison(self) -> None:
        self._poisoned = False

    def __enter__(self) -> MutexGuard:
        return self.lock()

    def __exit__(self, *_: Any) -> None:
        self._lock.release()

    def __repr__(self) -> str:
        return f"Mutex({self._value!r})"
