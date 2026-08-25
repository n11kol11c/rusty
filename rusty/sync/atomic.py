"""Atomic types — lock-free AtomicBool, AtomicInt, and generic Atomic."""
from __future__ import annotations
"""Atomic types — lock-free thread-safe primitives.

Provides Atomic[T], AtomicBool, and AtomicInt for atomic load, store,
swap, compare-and-set, and arithmetic operations.
"""

import threading
from typing import Generic, TypeVar

T = TypeVar("T")


class Atomic(Generic[T]):
    __slots__ = ("_value", "_lock")

    def __init__(self, value: T) -> None:
        self._value = value
        self._lock = threading.Lock()

    @classmethod
    def new(cls, value: T) -> Atomic[T]:
        return cls(value)

    def load(self) -> T:
        with self._lock:
            return self._value

    def store(self, value: T) -> None:
        with self._lock:
            self._value = value

    def swap(self, value: T) -> T:
        with self._lock:
            old = self._value
            self._value = value
            return old

    def into_inner(self) -> T:
        return self._value

    def __repr__(self) -> str:
        return f"Atomic({self._value!r})"


class AtomicBool:
    __slots__ = ("_value", "_lock")

    def __init__(self, value: bool = False) -> None:
        self._value = value
        self._lock = threading.Lock()

    @classmethod
    def new(cls, value: bool = False) -> AtomicBool:
        return cls(value)

    def load(self) -> bool:
        with self._lock:
            return self._value

    def store(self, value: bool) -> None:
        with self._lock:
            self._value = value

    def swap(self, value: bool) -> bool:
        with self._lock:
            old = self._value
            self._value = value
            return old

    def compare_and_set(self, current: bool, new: bool) -> bool:
        with self._lock:
            if self._value == current:
                self._value = new
                return True
            return False

    def fetch_and(self, value: bool) -> bool:
        with self._lock:
            old = self._value
            self._value = self._value and value
            return old

    def fetch_or(self, value: bool) -> bool:
        with self._lock:
            old = self._value
            self._value = self._value or value
            return old

    def fetch_xor(self, value: bool) -> bool:
        with self._lock:
            old = self._value
            self._value = self._value != value
            return old

    def into_inner(self) -> bool:
        return self._value

    def __repr__(self) -> str:
        return f"AtomicBool({self._value!r})"

    def __bool__(self) -> bool:
        return self.load()


class AtomicInt:
    __slots__ = ("_value", "_lock")

    def __init__(self, value: int = 0) -> None:
        self._value = value
        self._lock = threading.Lock()

    @classmethod
    def new(cls, value: int = 0) -> AtomicInt:
        return cls(value)

    def load(self) -> int:
        with self._lock:
            return self._value

    def store(self, value: int) -> None:
        with self._lock:
            self._value = value

    def swap(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value = value
            return old

    def fetch_add(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value += value
            return old

    def fetch_sub(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value -= value
            return old

    def fetch_and(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value &= value
            return old

    def fetch_or(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value |= value
            return old

    def fetch_xor(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value ^= value
            return old

    def compare_and_set(self, current: int, new: int) -> bool:
        with self._lock:
            if self._value == current:
                self._value = new
                return True
            return False

    def into_inner(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return f"AtomicInt({self._value!r})"

    def __int__(self) -> int:
        return self.load()

    def __add__(self, other: int) -> int:
        return self.load() + other

    def __sub__(self, other: int) -> int:
        return self.load() - other

    def __iadd__(self, other: int) -> AtomicInt:
        self.fetch_add(other)
        return self

    def __isub__(self, other: int) -> AtomicInt:
        self.fetch_sub(other)
        return self
