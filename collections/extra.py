"""Drain, IntoIter, Slice — supporting iterator types for collections."""
from __future__ import annotations
"""Supporting collection types — Drain, IntoIter, Slice.

Provides iterator types for consuming and borrowing collection contents.
"""

from typing import Generic, Iterable, Iterator, Sequence, TypeVar

T = TypeVar("T")


class Drain(Generic[T]):
    __slots__ = ("_source", "_index")

    def __init__(self, source: list[T]) -> None:
        self._source = source
        self._index = 0

    def __iter__(self) -> Iterator[T]:
        while self._index < len(self._source):
            yield self._source[self._index]
            self._index += 1
        self._source.clear()

    def __next__(self) -> T:
        if self._index >= len(self._source):
            raise StopIteration
        value = self._source[self._index]
        self._index += 1
        return value

    def __repr__(self) -> str:
        return f"Drain(remaining={len(self._source) - self._index})"


class IntoIter(Generic[T]):
    __slots__ = ("_iter",)

    def __init__(self, source: Iterable[T]) -> None:
        self._iter = iter(source)

    def __iter__(self) -> Iterator[T]:
        return self._iter

    def __next__(self) -> T:
        return next(self._iter)

    def __repr__(self) -> str:
        return "IntoIter(...)"


class Slice(Generic[T]):
    __slots__ = ("_data", "_start", "_end")

    def __init__(self, data: Sequence[T], start: int = 0, end: int | None = None) -> None:
        self._data = data
        self._start = start
        self._end = end if end is not None else len(data)

    @classmethod
    def from_list(cls, data: Sequence[T]) -> Slice[T]:
        return cls(data)

    def get(self, index: int) -> T:
        return self._data[self._start + index]

    def first(self) -> T | None:
        if self._start >= self._end:
            return None
        return self._data[self._start]

    def last(self) -> T | None:
        if self._start >= self._end:
            return None
        return self._data[self._end - 1]

    def len(self) -> int:
        return self._end - self._start

    def is_empty(self) -> bool:
        return self._start >= self._end

    def contains(self, value: T) -> bool:
        for i in range(self._start, self._end):
            if self._data[i] == value:
                return True
        return False

    def split_at(self, mid: int) -> tuple[Slice[T], Slice[T]]:
        return (
            Slice(self._data, self._start, self._start + mid),
            Slice(self._data, self._start + mid, self._end),
        )

    def iter(self) -> Iterator[T]:
        for i in range(self._start, self._end):
            yield self._data[i]

    def to_list(self) -> list[T]:
        return list(self._data[self._start:self._end])

    def __len__(self) -> int:
        return self.len()

    def __iter__(self) -> Iterator[T]:
        return self.iter()

    def __getitem__(self, index: int) -> T:
        return self.get(index)

    def __contains__(self, value: object) -> bool:
        return self.contains(value)  # type: ignore[arg-type]

    def __repr__(self) -> str:
        return f"Slice({self.to_list()})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Slice):
            return self.to_list() == other.to_list()
        if isinstance(other, (list, tuple)):
            return self.to_list() == list(other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self._data[self._start:self._end]))
