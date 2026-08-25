"""BinaryHeap — a max-heap priority queue."""
from __future__ import annotations
"""BinaryHeap — a priority queue.

Provides BinaryHeap with push, pop (returns max), peek,
and heapify operations.
"""

from typing import Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


class BinaryHeap(Generic[T]):
    __slots__ = ("_data", "_reverse")

    def __init__(self, values: Iterable[T] | None = None, *, reverse: bool = False) -> None:
        self._data: list[T] = list(values) if values else []
        self._reverse = reverse
        self._data.sort(reverse=not reverse)

    @classmethod
    def new(cls) -> BinaryHeap[T]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> BinaryHeap[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T], *, reverse: bool = False) -> BinaryHeap[T]:
        return cls(values, reverse=reverse)

    def push(self, value: T) -> None:
        self._data.append(value)
        self._data.sort(reverse=not self._reverse)

    def pop(self) -> T | None:
        if self._data:
            return self._data.pop(0)
        return None

    def peek(self) -> T | None:
        return self._data[0] if self._data else None

    def push_pop(self, push_value: T) -> T:
        self.push(push_value)
        return self.pop()  # type: ignore

    def peek_mut(self) -> T | None:
        return self.peek()

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    def contains(self, value: T) -> bool:
        return value in self._data

    def drain(self) -> Iterator[T]:
        items = sorted(self._data, reverse=not self._reverse)
        self._data.clear()
        return iter(items)

    def iter(self) -> Iterator[T]:
        return iter(sorted(self._data, reverse=not self._reverse))

    def to_list(self) -> list[T]:
        return sorted(self._data, reverse=not self._reverse)

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return self.iter()

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"BinaryHeap({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BinaryHeap):
            return sorted(self._data) == sorted(other._data)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(sorted(self._data)))

    def __bool__(self) -> bool:
        return bool(self._data)
