"""Range types — Range, RangeInclusive, RangeFrom, RangeTo, RangeToInclusive, RangeFull."""
from __future__ import annotations

"""Range types — Python equivalents of Rust range syntax.

Provides Range, RangeInclusive, RangeFrom, RangeTo, RangeToInclusive, RangeFull
with factory functions for constructing range objects.
"""

from typing import Generic, Iterator, TypeVar


T = TypeVar("T")


class Range(Generic[T]):
    __slots__ = ("start", "end")

    def __init__(self, start: T, end: T) -> None:
        self.start = start
        self.end = end

    def contains(self, value: T) -> bool:
        return self.start <= value < self.end

    def contains_inclusive(self, value: T) -> bool:
        return self.start <= value <= self.end

    def is_empty(self) -> bool:
        return self.start >= self.end

    def iter(self) -> Iterator[T]:
        yield from range(int(self.start), int(self.end))

    def __iter__(self) -> Iterator[T]:
        yield from range(int(self.start), int(self.end))

    def __len__(self) -> int:
        return max(0, int(self.end) - int(self.start))

    def __contains__(self, value: T) -> bool:
        return self.start <= value < self.end

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Range):
            return self.start == other.start and self.end == other.end
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __repr__(self) -> str:
        return f"{self.start}..{self.end}"


class RangeInclusive(Generic[T]):
    __slots__ = ("start", "end")

    def __init__(self, start: T, end: T) -> None:
        self.start = start
        self.end = end

    def contains(self, value: T) -> bool:
        return self.start <= value <= self.end

    def is_empty(self) -> bool:
        return self.start > self.end

    def iter(self) -> Iterator[T]:
        yield from range(int(self.start), int(self.end) + 1)

    def __iter__(self) -> Iterator[T]:
        yield from range(int(self.start), int(self.end) + 1)

    def __len__(self) -> int:
        return max(0, int(self.end) - int(self.start) + 1)

    def __contains__(self, value: T) -> bool:
        return self.start <= value <= self.end

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeInclusive):
            return self.start == other.start and self.end == other.end
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __repr__(self) -> str:
        return f"{self.start}..={self.end}"


class RangeFrom(Generic[T]):
    __slots__ = ("start",)

    def __init__(self, start: T) -> None:
        self.start = start

    def contains(self, value: T) -> bool:
        return value >= self.start

    def iter(self, end: T) -> Iterator[T]:
        yield from range(int(self.start), int(end))

    def __contains__(self, value: T) -> bool:
        return value >= self.start

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeFrom):
            return self.start == other.start
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.start)

    def __repr__(self) -> str:
        return f"{self.start}.."


class RangeTo(Generic[T]):
    __slots__ = ("end",)

    def __init__(self, end: T) -> None:
        self.end = end

    def contains(self, value: T) -> bool:
        return value < self.end

    def iter(self, start: T = 0) -> Iterator[T]:
        yield from range(int(start), int(self.end))

    def __contains__(self, value: T) -> bool:
        return value < self.end

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeTo):
            return self.end == other.end
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.end)

    def __repr__(self) -> str:
        return f"..{self.end}"


class RangeToInclusive(Generic[T]):
    __slots__ = ("end",)

    def __init__(self, end: T) -> None:
        self.end = end

    def contains(self, value: T) -> bool:
        return value <= self.end

    def iter(self, start: T = 0) -> Iterator[T]:
        yield from range(int(start), int(self.end) + 1)

    def __contains__(self, value: T) -> bool:
        return value <= self.end

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeToInclusive):
            return self.end == other.end
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.end)

    def __repr__(self) -> str:
        return f"..={self.end}"


class RangeFull:
    __slots__ = ()

    def contains(self, value: object) -> bool:
        return True

    def __contains__(self, value: object) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeFull):
            return True
        return NotImplemented

    def __hash__(self) -> int:
        return hash(None)

    def __repr__(self) -> str:
        return ".."


def range_(start: T, end: T) -> Range[T]:
    return Range(start, end)


def range_inclusive(start: T, end: T) -> RangeInclusive[T]:
    return RangeInclusive(start, end)


def range_from(start: T) -> RangeFrom[T]:
    return RangeFrom(start)


def range_to(end: T) -> RangeTo[T]:
    return RangeTo(end)


def range_to_inclusive(end: T) -> RangeToInclusive[T]:
    return RangeToInclusive(end)
