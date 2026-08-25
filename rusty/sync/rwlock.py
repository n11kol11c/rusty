"""RwLock — readers-writer lock with read/write guards."""
from __future__ import annotations
"""RwLock — readers-writer lock.

Provides RwLock[T] with RwLockReadGuard and RwLockWriteGuard for
concurrent reads with exclusive writes.
"""

import threading
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class RwLockReadGuard(Generic[T]):
    __slots__ = ("_lock",)

    def __init__(self, lock: RwLock) -> None:
        self._lock = lock

    @property
    def value(self) -> Any:
        return self._lock._value

    def release(self) -> None:
        self._lock._readers -= 1

    def __enter__(self) -> RwLockReadGuard[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"RwLockReadGuard({self._lock._value!r})"


class RwLockWriteGuard(Generic[T]):
    __slots__ = ("_lock",)

    def __init__(self, lock: RwLock) -> None:
        self._lock = lock

    @property
    def value(self) -> Any:
        return self._lock._value

    @value.setter
    def value(self, v: Any) -> None:
        self._lock._value = v

    def replace(self, v: Any) -> Any:
        old = self._lock._value
        self._lock._value = v
        return old

    def release(self) -> None:
        self._lock._writing = False
        self._lock._write_lock.release()

    def __enter__(self) -> RwLockWriteGuard[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"RwLockWriteGuard({self._lock._value!r})"


class RwLock(Generic[T]):
    __slots__ = ("_value", "_readers", "_writing", "_read_lock", "_write_lock", "_cond")

    def __init__(self, value: T) -> None:
        self._value = value
        self._readers = 0
        self._writing = False
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._cond = threading.Condition(threading.Lock())

    @classmethod
    def new(cls, value: T) -> RwLock[T]:
        return cls(value)

    def read(self) -> RwLockReadGuard[T]:
        with self._cond:
            while self._writing:
                self._cond.wait()
            self._readers += 1
        return RwLockReadGuard(self)

    def write(self) -> RwLockWriteGuard[T]:
        self._write_lock.acquire()
        with self._cond:
            while self._writing or self._readers > 0:
                self._cond.wait()
            self._writing = True
        return RwLockWriteGuard(self)

    def try_read(self) -> RwLockReadGuard[T] | None:
        with self._cond:
            if not self._writing:
                self._readers += 1
                return RwLockReadGuard(self)
        return None

    def try_write(self) -> RwLockWriteGuard[T] | None:
        if self._write_lock.acquire(blocking=False):
            with self._cond:
                if not self._writing and self._readers == 0:
                    self._writing = True
                    return RwLockWriteGuard(self)
            self._write_lock.release()
        return None

    def into_inner(self) -> T:
        return self._value

    def __repr__(self) -> str:
        return f"RwLock({self._value!r})"
