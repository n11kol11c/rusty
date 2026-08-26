"""BTreeSet — an ordered set with sorted iteration."""
from __future__ import annotations
"""BTreeSet — an ordered set.

Provides BTreeSet with keys maintained in sorted order for
efficient range queries and ordered iteration.
"""

from typing import Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


class BTreeSet(Generic[T]):
    __slots__ = ("_data",)

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._data: set[T] = set()
        if values is not None:
            for v in values:
                self._data.add(v)

    @classmethod
    def new(cls) -> BTreeSet[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> BTreeSet[T]:
        return cls(values)

    def insert(self, value: T) -> bool:
        existed = value in self._data
        self._data.add(value)
        return not existed

    def remove(self, value: T) -> bool:
        if value in self._data:
            self._data.remove(value)
            return True
        return False

    def contains(self, value: T) -> bool:
        return value in self._data

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    def first(self) -> T | None:
        if not self._data:
            return None
        return min(self._data)

    def last(self) -> T | None:
        if not self._data:
            return None
        return max(self._data)

    def iter(self) -> Iterator[T]:
        return iter(sorted(self._data))

    def range_(self, start: T, end: T) -> Iterator[T]:
        for v in sorted(self._data):
            if start <= v < end:
                yield v

    def intersection(self, other: BTreeSet[T]) -> BTreeSet[T]:
        return BTreeSet(self._data & other._data)

    def union(self, other: BTreeSet[T]) -> BTreeSet[T]:
        return BTreeSet(self._data | other._data)

    def difference(self, other: BTreeSet[T]) -> BTreeSet[T]:
        return BTreeSet(self._data - other._data)

    def symmetric_difference(self, other: BTreeSet[T]) -> BTreeSet[T]:
        return BTreeSet(self._data ^ other._data)

    def is_disjoint(self, other: BTreeSet[T]) -> bool:
        return self._data.isdisjoint(other._data)

    def is_subset(self, other: BTreeSet[T]) -> bool:
        return self._data.issubset(other._data)

    def is_superset(self, other: BTreeSet[T]) -> bool:
        return self._data.issuperset(other._data)

    def to_list(self) -> list[T]:
        return sorted(self._data)

    def to_set(self) -> set[T]:
        return self._data.copy()

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return self.iter()

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"BTreeSet({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BTreeSet):
            return self._data == other._data
        return NotImplemented

    def __hash__(self) -> int:
        return hash(frozenset(self._data))

    def __bool__(self) -> bool:
        return bool(self._data)
