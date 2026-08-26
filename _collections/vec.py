"""Vec — a growable array with push, pop, insert, remove, drain, and list protocol support."""
from __future__ import annotations
"""Vec — a growable array type.

Provides Vec[T] with push, pop, insert, remove, retain, drain,
iter, and Python list protocol support.
"""

from typing import Any, Callable, Generic, Iterable, Iterator, TypeVar, overload

from ..core.option import Option, Some, None_

T = TypeVar("T")


class Vec(Generic[T]):
    __slots__ = ("_data", "_capacity")

    def __init__(
        self,
        values: Iterable[T] = (),
        *,
        capacity: int | None = None,
    ) -> None:
        self._data = list(values)

        if capacity is None:
            self._capacity = len(self._data)
        else:
            if capacity < len(self._data):
                raise ValueError(
                    "capacity cannot be smaller than length"
                )

            self._capacity = capacity

    @classmethod
    def new(cls) -> Vec[T]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> Vec[T]:
        if capacity < 0:
            raise ValueError("capacity must be non-negative")

        return cls(capacity=capacity)

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> Vec[T]:
        return cls(values)

    @classmethod
    def repeat(cls, value: T, n: int) -> Vec[T]:
        if n < 0:
            raise ValueError("n must be non-negative")

        return cls([value] * n)

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def capacity(self) -> int:
        return self._capacity


    def reserve(self, additional: int) -> None:
        if additional < 0:
            raise ValueError("additional must be non-negative")

        required = self.len() + additional

        if required <= self._capacity:
            return

        new_capacity = max(
            required,
            max(1, self._capacity * 2),
        )

        self._capacity = new_capacity

    def reserve_exact(self, additional: int) -> None:
        if additional < 0:
            raise ValueError("additional must be non-negative")

        required = self.len() + additional

        if required > self._capacity:
            self._capacity = required

    def shrink_to_fit(self) -> None:
        self._capacity = self.len()

    def shrink_to(self, min_capacity: int) -> None:
        if min_capacity < 0:
            raise ValueError(
                "min_capacity must be non-negative"
            )

        self._capacity = max(
            self.len(),
            min_capacity,
        )

    def push(self, value: T) -> None:
        self.reserve(1)
        self._data.append(value)

    def pop(self) -> Option[T]:
        if not self._data:
            return None_

        return Some(self._data.pop())

    def insert(self, index: int, value: T) -> None:
        if index < 0 or index > self.len():
            raise IndexError(
                f"index {index} out of bounds"
            )

        self.reserve(1)
        self._data.insert(index, value)

    def remove(self, index: int) -> T:
        self._check_index(index)
        return self._data.pop(index)

    def swap_remove(self, index: int) -> T:
        self._check_index(index)

        last = self._data.pop()

        if index == self.len():
            return last

        removed = self._data[index]
        self._data[index] = last

        return removed

    def clear(self) -> None:
        self._data.clear()

    def truncate(self, length: int) -> None:
        if length < 0:
            raise ValueError(
                "length must be non-negative"
            )

        del self._data[length:]


    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self.len():
            raise IndexError(
                f"index {index} out of bounds "
                f"for Vec of length {self.len()}"
            )

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Vec[T]:
        ...

    def __getitem__(
        self,
        index: int | slice,
    ) -> T | Vec[T]:

        if isinstance(index, slice):
            return Vec(self._data[index])

        self._check_index(index)
        return self._data[index]

    def get(self, index: int) -> Option[T]:
        if index < 0 or index >= self.len():
            return None_

        return Some(self._data[index])

    def first(self) -> Option[T]:
        if not self._data:
            return None_

        return Some(self._data[0])

    def last(self) -> Option[T]:
        if not self._data:
            return None_

        return Some(self._data[-1])

    def contains(self, value: T) -> bool:
        return value in self._data

    def position(
        self,
        predicate: Callable[[T], bool],
    ) -> Option[int]:

        for index, value in enumerate(self._data):
            if predicate(value):
                return Some(index)

        return None_

    def find(
        self,
        predicate: Callable[[T], bool],
    ) -> Option[T]:

        for value in self._data:
            if predicate(value):
                return Some(value)

        return None_

    def reverse(self) -> None:
        self._data.reverse()

    def sort(
        self,
        *,
        key: Callable[[T], Any] | None = None,
        reverse: bool = False,
    ) -> None:

        self._data.sort(
            key=key,
            reverse=reverse,
        )

    def sort_unstable(
        self,
        *,
        key: Callable[[T], Any] | None = None,
        reverse: bool = False,
    ) -> None:

        self._data.sort(
            key=key,
            reverse=reverse,
        )

    def retain(
        self,
        predicate: Callable[[T], bool],
    ) -> None:

        self._data[:] = [
            value
            for value in self._data
            if predicate(value)
        ]

    def dedup(self) -> None:
        if len(self._data) < 2:
            return

        result = [self._data[0]]

        for value in self._data[1:]:
            if value != result[-1]:
                result.append(value)

        self._data[:] = result

    def append(self, other: Vec[T]) -> None:
        self.reserve(other.len())
        self._data.extend(other._data)

    def extend(
        self,
        values: Iterable[T],
    ) -> None:

        values = list(values)

        self.reserve(len(values))
        self._data.extend(values)

    def split_off(self, at: int) -> Vec[T]:
        if at < 0 or at > self.len():
            raise IndexError(
                f"split index {at} out of bounds"
            )

        result = Vec(self._data[at:])
        del self._data[at:]

        return result

    def iter(self) -> Iterator[T]:
        return iter(self._data)

    def enumerate(self) -> Iterator[tuple[int, T]]:
        return enumerate(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def to_list(self) -> list[T]:
        return self._data.copy()

    def into_iter(self) -> Iterator[T]:
        data = self._data

        self._data = []
        self._capacity = 0

        return iter(data)

    def __len__(self) -> int:
        return self.len()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"Vec({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vec):
            return self._data == other._data

        return NotImplemented
