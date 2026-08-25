"""Core iterator types — Iter, PeekableIter, and Range types."""
from __future__ import annotations

"""Core iterator types.

Provides Iter for wrapping iterables and PeekableIter for lookahead iteration.
Also includes Range types for numeric iteration.
"""

from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    TypeVar,
)

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


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


class Iter(Generic[T]):
    __slots__ = ("_iter",)

    def __init__(self, source: Iterable[T] | Iterator[T]) -> None:
        if isinstance(source, Iterator):
            self._iter = source
        else:
            self._iter = iter(source)

    @classmethod
    def from_fn(cls, fn: Callable[[int], T], start: int = 0) -> Iter[T]:
        def gen():
            i = start
            while True:
                yield fn(i)
                i += 1
        return cls(gen())

    @classmethod
    def repeat(cls, value: T) -> Iter[T]:
        def gen():
            while True:
                yield value
        return cls(gen())

    @classmethod
    def count(cls, start: int = 0, step: int = 1) -> Iter[int]:
        def gen():
            i = start
            while True:
                yield i
                i += step
        return cls(gen())

    @classmethod
    def zip(cls, a: Iterable[T], b: Iterable[U]) -> Iter[tuple[T, U]]:
        return cls(zip(a, b))

    @classmethod
    def chain(cls, *iters: Iterable[T]) -> Iter[T]:
        def gen():
            for it in iters:
                yield from it
        return cls(gen())

    def map(self, fn: Callable[[T], U]) -> Iter[U]:
        def gen():
            for v in self._iter:
                yield fn(v)
        return Iter(gen())

    def map_enumerate(self, fn: Callable[[int, T], U]) -> Iter[U]:
        def gen():
            for i, v in enumerate(self._iter):
                yield fn(i, v)
        return Iter(gen())

    def filter(self, predicate: Callable[[T], bool]) -> Iter[T]:
        def gen():
            for v in self._iter:
                if predicate(v):
                    yield v
        return Iter(gen())

    def filter_map(self, fn: Callable[[T], U | None]) -> Iter[U]:
        def gen():
            for v in self._iter:
                result = fn(v)
                if result is not None:
                    yield result
        return Iter(gen())

    def enumerate(self, start: int = 0) -> Iter[tuple[int, T]]:
        def gen():
            for i, v in enumerate(self._iter, start):
                yield (i, v)
        return Iter(gen())

    def peekable(self) -> PeekableIter[T]:
        return PeekableIter(self._iter)

    def take(self, n: int) -> Iter[T]:
        def gen():
            for i, v in enumerate(self._iter):
                if i >= n:
                    break
                yield v
        return Iter(gen())

    def take_while(self, predicate: Callable[[T], bool]) -> Iter[T]:
        def gen():
            for v in self._iter:
                if not predicate(v):
                    break
                yield v
        return Iter(gen())

    def skip(self, n: int) -> Iter[T]:
        def gen():
            for i, v in enumerate(self._iter):
                if i >= n:
                    yield v
        return Iter(gen())

    def skip_while(self, predicate: Callable[[T], bool]) -> Iter[T]:
        def gen():
            skipping = True
            for v in self._iter:
                if skipping and predicate(v):
                    continue
                skipping = False
                yield v
        return Iter(gen())

    def flat_map(self, fn: Callable[[T], Iterable[U]]) -> Iter[U]:
        def gen():
            for v in self._iter:
                yield from fn(v)
        return Iter(gen())

    def flatten(self) -> Iter[Any]:
        def gen():
            for v in self._iter:
                if hasattr(v, '__iter__'):
                    yield from v
                else:
                    yield v
        return Iter(gen())

    def inspect(self, fn: Callable[[T], Any]) -> Iter[T]:
        def gen():
            for v in self._iter:
                fn(v)
                yield v
        return Iter(gen())

    def step_by(self, step: int) -> Iter[T]:
        def gen():
            for i, v in enumerate(self._iter):
                if i % step == 0:
                    yield v
        return Iter(gen())

    def zip_with(self, other: Iterable[U], fn: Callable[[T, U], V]) -> Iter[V]:
        def gen():
            for a, b in zip(self._iter, other):
                yield fn(a, b)
        return Iter(gen())

    def fuse(self) -> Iter[T]:
        def gen():
            exhausted = False
            for v in self._iter:
                if exhausted:
                    break
                yield v
        return Iter(gen())

    def fold(self, init: U, fn: Callable[[U, T], U]) -> U:
        acc = init
        for v in self._iter:
            acc = fn(acc, v)
        return acc

    def reduce(self, fn: Callable[[T, T], T]) -> T | None:
        it = iter(self._iter)
        try:
            acc = next(it)
        except StopIteration:
            return None
        for v in it:
            acc = fn(acc, v)
        return acc

    def collect(self) -> list[T]:
        return list(self._iter)

    def collect_into(self, collection: Any) -> Any:
        for v in self._iter:
            collection.append(v)
        return collection

    def count(self) -> int:
        n = 0
        for _ in self._iter:
            n += 1
        return n

    def sum(self) -> T:
        return self.fold(0, lambda a, b: a + b)  # type: ignore

    def product(self) -> T:
        return self.fold(1, lambda a, b: a * b)  # type: ignore

    def min(self) -> T | None:
        return self.reduce(lambda a, b: a if a < b else b)

    def max(self) -> T | None:
        return self.reduce(lambda a, b: a if a > b else b)

    def all(self, predicate: Callable[[T], bool]) -> bool:
        for v in self._iter:
            if not predicate(v):
                return False
        return True

    def any(self, predicate: Callable[[T], bool]) -> bool:
        for v in self._iter:
            if predicate(v):
                return True
        return False

    def position(self, predicate: Callable[[T], bool]) -> int | None:
        for i, v in enumerate(self._iter):
            if predicate(v):
                return i
        return None

    def nth(self, n: int) -> T | None:
        for i, v in enumerate(self._iter):
            if i == n:
                return v
        return None

    def last(self) -> T | None:
        result = None
        for v in self._iter:
            result = v
        return result

    def next(self) -> T:
        return next(self._iter)

    def for_each(self, fn: Callable[[T], Any]) -> None:
        for v in self._iter:
            fn(v)

    def partition(self, predicate: Callable[[T], bool]) -> tuple[list[T], list[T]]:
        a, b = [], []
        for v in self._iter:
            (a if predicate(v) else b).append(v)
        return a, b

    def __iter__(self) -> Iterator[T]:
        return self._iter

    def __next__(self) -> T:
        return next(self._iter)

    def __repr__(self) -> str:
        return "Iter(...)"


class PeekableIter(Generic[T]):
    __slots__ = ("_iter", "_peeked", "_has_peeked")

    def __init__(self, source: Iterator[T]) -> None:
        self._iter = source
        self._peeked: T = None  # type: ignore[assignment]
        self._has_peeked = False

    def peek(self) -> T | None:
        if self._has_peeked:
            return self._peeked
        try:
            self._peeked = next(self._iter)
            self._has_peeked = True
            return self._peeked
        except StopIteration:
            return None

    def next(self) -> T:
        if self._has_peeked:
            self._has_peeked = False
            return self._peeked
        return next(self._iter)

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        return self.next()
