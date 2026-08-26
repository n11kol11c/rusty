"""BTreeMap — an ordered map with sorted key iteration."""
from __future__ import annotations
"""BTreeMap — an ordered key-value map.

Provides BTreeMap with keys maintained in sorted order for
efficient range queries and ordered iteration.
"""

from typing import Generic, Iterable, Iterator, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class BTreeMap(Generic[K, V]):
    __slots__ = ("_data",)

    def __init__(self, values: Iterable[tuple[K, V]] | dict[K, V] | None = None) -> None:
        self._data: dict[K, V] = {}
        if values is not None:
            if isinstance(values, dict):
                self._data = dict(sorted(values.items()))
            else:
                self._data = dict(sorted(values, key=lambda x: x[0]))

    @classmethod
    def new(cls) -> BTreeMap[K, V]:
        return cls()

    @classmethod
    def from_dict(cls, values: dict[K, V]) -> BTreeMap[K, V]:
        return cls(values)

    def insert(self, key: K, value: V) -> V | None:
        old = self._data.get(key)
        self._data[key] = value
        return old

    def get(self, key: K) -> V | None:
        return self._data.get(key)

    def get_key_value(self, key: K) -> tuple[K, V] | None:
        if key in self._data:
            return (key, self._data[key])
        return None

    def remove(self, key: K) -> V | None:
        return self._data.pop(key, None)

    def contains_key(self, key: K) -> bool:
        return key in self._data

    def first_key_value(self) -> tuple[K, V] | None:
        if not self._data:
            return None
        key = min(self._data.keys())
        return (key, self._data[key])

    def last_key_value(self) -> tuple[K, V] | None:
        if not self._data:
            return None
        key = max(self._data.keys())
        return (key, self._data[key])

    def clear(self) -> None:
        self._data.clear()

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def keys(self) -> Iterator[K]:
        return iter(sorted(self._data.keys()))

    def values(self) -> Iterator[V]:
        for k in sorted(self._data.keys()):
            yield self._data[k]

    def iter(self) -> Iterator[tuple[K, V]]:
        for k in sorted(self._data.keys()):
            yield (k, self._data[k])

    def drain(self) -> Iterator[tuple[K, V]]:
        items = sorted(self._data.items())
        self._data.clear()
        return iter(items)

    def range_(self, start: K, end: K) -> Iterator[tuple[K, V]]:
        for k in sorted(self._data.keys()):
            if start <= k < end:
                yield (k, self._data[k])

    def to_dict(self) -> dict[K, V]:
        return dict(sorted(self._data.items()))

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[K]:
        return self.keys()

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __getitem__(self, key: K) -> V:
        return self._data[key]

    def __setitem__(self, key: K, value: V) -> None:
        self._data[key] = value

    def __delitem__(self, key: K) -> None:
        del self._data[key]

    def __repr__(self) -> str:
        return f"BTreeMap({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BTreeMap):
            return self._data == other._data
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(sorted(self._data.items())))

    def __bool__(self) -> bool:
        return bool(self._data)
