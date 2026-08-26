"""HashMap — a hash map with Entry API for efficient in-place manipulation."""
from __future__ import annotations
"""HashMap — a hash-based key-value map.

Provides HashMap with Entry API (OccupiedEntry, VacantEntry) for
efficient in-place manipulation of map entries.
"""

from typing import Callable, Generic, Iterable, Iterator, TypeVar

from ..core.option import Option, Some, None_

K = TypeVar("K")
V = TypeVar("V")
U = TypeVar("U")


class _Missing:
    __slots__ = ()


_MISSING = _Missing()


class HashMap(Generic[K, V]):
    __slots__ = ("_data", "_capacity")

    def __init__(
        self,
        values: Iterable[tuple[K, V]] | dict[K, V] | None = None,
        *,
        capacity: int = 0,
    ) -> None:
        if capacity < 0:
            raise ValueError("capacity must be non-negative")

        self._data: dict[K, V] = {}
        self._capacity = max(capacity, 0)

        if values is not None:
            if isinstance(values, dict):
                self.extend(values.items())
            else:
                self.extend(values)

    @classmethod
    def new(cls) -> HashMap[K, V]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> HashMap[K, V]:
        return cls(capacity=capacity)

    @classmethod
    def from_iter(
        cls,
        values: Iterable[tuple[K, V]],
    ) -> HashMap[K, V]:
        return cls(values)

    @classmethod
    def from_dict(
        cls,
        values: dict[K, V],
    ) -> HashMap[K, V]:
        return cls(values.items())

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def capacity(self) -> int:
        return max(self._capacity, len(self._data))

    def reserve(self, additional: int) -> None:
        if additional < 0:
            raise ValueError("additional must be non-negative")

        required = self.len() + additional

        if required > self._capacity:
            self._capacity = max(
                required,
                max(1, self._capacity * 2),
            )

    def reserve_exact(self, additional: int) -> None:
        if additional < 0:
            raise ValueError("additional must be non-negative")

        required = self.len() + additional

        if required > self._capacity:
            self._capacity = required

    def try_reserve(self, additional: int) -> bool:
        try:
            self.reserve(additional)
            return True
        except (MemoryError, OverflowError):
            return False

    def shrink_to_fit(self) -> None:
        self._capacity = self.len()

    def shrink_to(self, min_capacity: int) -> None:
        if min_capacity < 0:
            raise ValueError("min_capacity must be non-negative")

        self._capacity = max(
            self.len(),
            min_capacity,
        )

    def insert(self, key: K, value: V) -> Option[V]:
        old = self._data.get(key, _MISSING)

        if old is _MISSING:
            self.reserve(1)
            self._data[key] = value
            return None_

        self._data[key] = value
        return Some(old)

    def insert_entry(self, key: K, value: V) -> OccupiedEntry[K, V]:
        self.insert(key, value)
        return OccupiedEntry(self, key)

    def get(self, key: K) -> Option[V]:
        value = self._data.get(key, _MISSING)

        if value is _MISSING:
            return None_

        return Some(value)

    def get_value(self, key: K) -> V | None:
        return self._data.get(key)

    def get_mut(self, key: K) -> Option[MutableValue[K, V]]:
        if key not in self._data:
            return None_

        return Some(MutableValue(self, key))

    def get_key_value(self, key: K) -> Option[tuple[K, V]]:
        if key not in self._data:
            return None_

        return Some((key, self._data[key]))

    def contains_key(self, key: K) -> bool:
        return key in self._data

    def remove(self, key: K) -> Option[V]:
        value = self._data.pop(key, _MISSING)

        if value is _MISSING:
            return None_

        return Some(value)

    def remove_entry(self, key: K) -> Option[tuple[K, V]]:
        if key not in self._data:
            return None_

        return Some((key, self._data.pop(key)))

    def clear(self) -> None:
        self._data.clear()

    def retain(self, predicate: Callable[[K, V], bool]) -> None:
        keys = [
            key
            for key, value in self._data.items()
            if not predicate(key, value)
        ]

        for key in keys:
            del self._data[key]

    def entry(self, key: K) -> Entry[K, V]:
        if key in self._data:
            return OccupiedEntry(self, key)

        return VacantEntry(self, key)

    def or_insert(self, key: K, value: V) -> V:
        entry = self.entry(key)
        return entry.or_insert(value)

    def or_insert_with(
        self,
        key: K,
        fn: Callable[[], V],
    ) -> V:
        entry = self.entry(key)
        return entry.or_insert_with(fn)

    def or_insert_with_key(
        self,
        key: K,
        fn: Callable[[K], V],
    ) -> V:
        entry = self.entry(key)
        return entry.or_insert_with_key(fn)

    def extend(
        self,
        values: Iterable[tuple[K, V]],
    ) -> None:
        values = list(values)
        self.reserve(len(values))

        for key, value in values:
            self._data[key] = value

    def extend_one(self, key: K, value: V) -> None:
        self.insert(key, value)

    def iter(self) -> Iterator[tuple[K, V]]:
        return iter(self._data.items())

    def iter_mut(self) -> Iterator[MutableValue[K, V]]:
        for key in self._data:
            yield MutableValue(self, key)

    def keys(self) -> Iterator[K]:
        return iter(self._data.keys())

    def values(self) -> Iterator[V]:
        return iter(self._data.values())

    def values_mut(self) -> Iterator[MutableValue[K, V]]:
        return self.iter_mut()

    def into_iter(self) -> Iterator[tuple[K, V]]:
        data = self._data

        self._data = {}
        self._capacity = 0

        return iter(data.items())

    def drain(self) -> Iterator[tuple[K, V]]:
        data = self._data

        self._data = {}
        self._capacity = 0

        return iter(data.items())

    def is_disjoint(self, other: HashMap[K, V]) -> bool:
        return not any(
            key in other._data
            for key in self._data
        )

    def len_common(self, other: HashMap[K, U]) -> int:
        return sum(
            key in other._data
            for key in self._data
        )

    def clone(self) -> HashMap[K, V]:
        result = HashMap[K, V]()
        result._data = self._data.copy()
        result._capacity = self._capacity
        return result

    def to_dict(self) -> dict[K, V]:
        return self._data.copy()

    def __getitem__(self, key: K) -> V:
        return self._data[key]

    def __setitem__(self, key: K, value: V) -> None:
        self.insert(key, value)

    def __delitem__(self, key: K) -> None:
        del self._data[key]

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __repr__(self) -> str:
        return f"HashMap({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HashMap):
            return self._data == other._data

        if isinstance(other, dict):
            return self._data == other

        return NotImplemented


class Entry(Generic[K, V]):
    __slots__ = ()

    def is_occupied(self) -> bool:
        return isinstance(self, OccupiedEntry)

    def is_vacant(self) -> bool:
        return isinstance(self, VacantEntry)

    def key(self) -> K:
        raise NotImplementedError

    def or_insert(self, value: V) -> V:
        raise NotImplementedError

    def or_insert_with(self, fn: Callable[[], V]) -> V:
        raise NotImplementedError

    def or_insert_with_key(
        self,
        fn: Callable[[K], V],
    ) -> V:
        raise NotImplementedError

    def and_modify(
        self,
        fn: Callable[[MutableValue[K, V]], None],
    ) -> Entry[K, V]:
        if isinstance(self, OccupiedEntry):
            fn(MutableValue(self._map, self._key))

        return self


class OccupiedEntry(Entry[K, V]):
    __slots__ = ("_map", "_key")

    def __init__(
        self,
        map_: HashMap[K, V],
        key: K,
    ) -> None:
        self._map = map_
        self._key = key

    def key(self) -> K:
        return self._key

    def get(self) -> V:
        return self._map._data[self._key]

    def get_mut(self) -> MutableValue[K, V]:
        return MutableValue(self._map, self._key)

    def insert(self, value: V) -> V:
        old = self._map._data[self._key]
        self._map._data[self._key] = value
        return old

    def remove(self) -> V:
        return self._map._data.pop(self._key)

    def remove_entry(self) -> tuple[K, V]:
        return self._key, self._map._data.pop(self._key)

    def or_insert(self, value: V) -> V:
        return self.get()

    def or_insert_with(self, fn: Callable[[], V]) -> V:
        return self.get()

    def or_insert_with_key(
        self,
        fn: Callable[[K], V],
    ) -> V:
        return self.get()


class VacantEntry(Entry[K, V]):
    __slots__ = ("_map", "_key")

    def __init__(
        self,
        map_: HashMap[K, V],
        key: K,
    ) -> None:
        self._map = map_
        self._key = key

    def key(self) -> K:
        return self._key

    def insert(self, value: V) -> V:
        self._map.insert(self._key, value)
        return value

    def or_insert(self, value: V) -> V:
        return self.insert(value)

    def or_insert_with(self, fn: Callable[[], V]) -> V:
        return self.insert(fn())

    def or_insert_with_key(
        self,
        fn: Callable[[K], V],
    ) -> V:
        return self.insert(fn(self._key))


class MutableValue(Generic[K, V]):
    __slots__ = ("_map", "_key")

    def __init__(
        self,
        map_: HashMap[K, V],
        key: K,
    ) -> None:
        self._map = map_
        self._key = key

    @property
    def value(self) -> V:
        return self._map._data[self._key]

    @value.setter
    def value(self, value: V) -> None:
        self._map._data[self._key] = value

    def replace(self, value: V) -> V:
        old = self.value
        self.value = value
        return old

    def get(self) -> V:
        return self.value

    def set(self, value: V) -> None:
        self.value = value
