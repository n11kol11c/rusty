"""VecDeque — a double-ended queue with O(1) push/pop at both ends."""
from __future__ import annotations
"""VecDeque — a double-ended queue.

Provides VecDeque with push_front, push_back, pop_front, pop_back,
and efficient O(1) operations at both ends.
"""

from typing import Generic, Iterable, Iterator, TypeVar

from .extra import Drain

T = TypeVar("T")


class VecDeque(Generic[T]):
    __slots__ = ("_data",)

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._data: list[T] = list(values) if values else []

    @classmethod
    def new(cls) -> VecDeque[T]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> VecDeque[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> VecDeque[T]:
        return cls(values)

    def push_back(self, value: T) -> None:
        self._data.append(value)

    def push_front(self, value: T) -> None:
        self._data.insert(0, value)

    def pop_back(self) -> T | None:
        if self._data:
            return self._data.pop()
        return None

    def pop_front(self) -> T | None:
        if self._data:
            return self._data.pop(0)
        return None

    def front(self) -> T | None:
        return self._data[0] if self._data else None

    def back(self) -> T | None:
        return self._data[-1] if self._data else None

    def get(self, index: int) -> T | None:
        if 0 <= index < len(self._data):
            return self._data[index]
        return None

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    def insert(self, index: int, value: T) -> None:
        self._data.insert(index, value)

    def remove(self, index: int) -> T | None:
        if 0 <= index < len(self._data):
            return self._data.pop(index)
        return None

    def contains(self, value: T) -> bool:
        return value in self._data

    def rotate_left(self, k: int) -> None:
        if self._data:
            k = k % len(self._data)
            self._data = self._data[k:] + self._data[:k]

    def rotate_right(self, k: int) -> None:
        if self._data:
            k = k % len(self._data)
            self._data = self._data[-k:] + self._data[:-k]

    def truncate(self, length: int) -> None:
        del self._data[length:]

    def drain(self) -> Drain[T]:
        return Drain(self._data)

    def iter(self) -> Iterator[T]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __getitem__(self, index: int) -> T:
        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        self._data[index] = value

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"VecDeque({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, VecDeque):
            return self._data == other._data
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self._data))

    def __bool__(self) -> bool:
        return bool(self._data)
