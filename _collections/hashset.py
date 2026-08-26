"""HashSet — a hash set with union, intersection, difference operations."""
from __future__ import annotations
"""HashSet — a hash-based set.

Provides HashSet with union, intersection, difference, symmetric_difference,
and all standard set operations.
"""

from typing import Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


class HashSet(Generic[T]):
    __slots__ = ("_data",)

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._data: set[T] = set()
        if values is not None:
            for v in values:
                self._data.add(v)

    @classmethod
    def new(cls) -> HashSet[T]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> HashSet[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> HashSet[T]:
        return cls(values)

    def insert(self, value: T) -> bool:
        existed = value in self._data
        self._data.add(value)
        return not existed

    def remove(self, value: T) -> T | None:
        return self._data.discard(value) or None if value in self._data else None

    def take(self, value: T) -> T | None:
        if value in self._data:
            self._data.remove(value)
            return value
        return None

    def contains(self, value: T) -> bool:
        return value in self._data

    def get(self, value: T) -> T | None:
        if value in self._data:
            return value
        return None

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    def iter(self) -> Iterator[T]:
        return iter(self._data)

    def drain(self) -> Iterator[T]:
        items = list(self._data)
        self._data.clear()
        return iter(items)

    def extend(self, values: Iterable[T]) -> None:
        for v in values:
            self._data.add(v)

    def intersection(self, other: HashSet[T]) -> HashSet[T]:
        return HashSet(self._data & other._data)

    def union(self, other: HashSet[T]) -> HashSet[T]:
        return HashSet(self._data | other._data)

    def difference(self, other: HashSet[T]) -> HashSet[T]:
        return HashSet(self._data - other._data)

    def symmetric_difference(self, other: HashSet[T]) -> HashSet[T]:
        return HashSet(self._data ^ other._data)

    def is_disjoint(self, other: HashSet[T]) -> bool:
        return self._data.isdisjoint(other._data)

    def is_subset(self, other: HashSet[T]) -> bool:
        return self._data.issubset(other._data)

    def is_superset(self, other: HashSet[T]) -> bool:
        return self._data.issuperset(other._data)

    def to_list(self) -> list[T]:
        return list(self._data)

    def to_set(self) -> set[T]:
        return self._data.copy()

    def into_iter(self) -> Iterator[T]:
        items = list(self._data)
        self._data.clear()
        return iter(items)

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"HashSet({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HashSet):
            return self._data == other._data
        return NotImplemented

    def __hash__(self) -> int:
        return hash(frozenset(self._data))

    def __bool__(self) -> bool:
        return bool(self._data)
