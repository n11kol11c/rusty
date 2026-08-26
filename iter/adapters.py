"""Iterator adapters — 18 adapters (Map, Filter, Take, Skip, Chain, etc.) for transforming iterables."""
from __future__ import annotations

"""Iterator adapters — transform and compose iterators.

Provides 18 adapter types: Enumerate, Zip, Map, Filter, FilterMap, FlatMap,
Flatten, Peekable, Fuse, Chain, Cycle, Take, Skip, Rev, Inspect, Copied,
Cloned, Partition. Each wraps an iterator and produces a new iterator.
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


class _EnumerateIterator(Generic[T]):
    __slots__ = ("_iter", "_index")

    def __init__(self, iterable: Iterable[T], start: int = 0) -> None:
        self._iter = iter(iterable)
        self._index = start

    def __iter__(self) -> _EnumerateIterator[T]:
        return self

    def __next__(self) -> tuple[int, T]:
        idx = self._index
        val = next(self._iter)
        self._index += 1
        return (idx, val)


class Enumerate(Generic[T]):
    __slots__ = ("_iterable", "_start")

    def __init__(self, iterable: Iterable[T], start: int = 0) -> None:
        self._iterable = iterable
        self._start = start

    def __iter__(self) -> _EnumerateIterator[T]:
        return _EnumerateIterator(self._iterable, self._start)

    def __repr__(self) -> str:
        return "Enumerate(...)"


class _ZipIterator(Generic[T, U]):
    __slots__ = ("_iter_a", "_iter_b")

    def __init__(self, a: Iterator[T], b: Iterator[U]) -> None:
        self._iter_a = a
        self._iter_b = b

    def __iter__(self) -> _ZipIterator[T, U]:
        return self

    def __next__(self) -> tuple[T, U]:
        return (next(self._iter_a), next(self._iter_b))


class Zip(Generic[T, U]):
    __slots__ = ("_iter_a", "_iter_b")

    def __init__(self, a: Iterable[T], b: Iterable[U]) -> None:
        self._iter_a = a
        self._iter_b = b

    def __iter__(self) -> _ZipIterator[T, U]:
        return _ZipIterator(iter(self._iter_a), iter(self._iter_b))

    def __repr__(self) -> str:
        return "Zip(...)"


class _MapIterator(Generic[T, U]):
    __slots__ = ("_iter", "_fn")

    def __init__(self, iterable: Iterator[T], fn: Callable[[T], U]) -> None:
        self._iter = iterable
        self._fn = fn

    def __iter__(self) -> _MapIterator[T, U]:
        return self

    def __next__(self) -> U:
        return self._fn(next(self._iter))


class Map(Generic[T, U]):
    __slots__ = ("_iterable", "_fn")

    def __init__(self, iterable: Iterable[T], fn: Callable[[T], U]) -> None:
        self._iterable = iterable
        self._fn = fn

    def __iter__(self) -> _MapIterator[T, U]:
        return _MapIterator(iter(self._iterable), self._fn)

    def __repr__(self) -> str:
        return "Map(...)"


class _FilterIterator(Generic[T]):
    __slots__ = ("_iter", "_pred")

    def __init__(self, iterable: Iterator[T], pred: Callable[[T], bool]) -> None:
        self._iter = iterable
        self._pred = pred

    def __iter__(self) -> _FilterIterator[T]:
        return self

    def __next__(self) -> T:
        while True:
            val = next(self._iter)
            if self._pred(val):
                return val


class Filter(Generic[T]):
    __slots__ = ("_iterable", "_pred")

    def __init__(self, iterable: Iterable[T], pred: Callable[[T], bool]) -> None:
        self._iterable = iterable
        self._pred = pred

    def __iter__(self) -> _FilterIterator[T]:
        return _FilterIterator(iter(self._iterable), self._pred)

    def __repr__(self) -> str:
        return "Filter(...)"


class _FilterMapIterator(Generic[T, U]):
    __slots__ = ("_iter", "_fn")

    def __init__(self, iterable: Iterator[T], fn: Callable[[T], U | None]) -> None:
        self._iter = iterable
        self._fn = fn

    def __iter__(self) -> _FilterMapIterator[T, U]:
        return self

    def __next__(self) -> U:
        while True:
            val = self._fn(next(self._iter))
            if val is not None:
                return val


class FilterMap(Generic[T, U]):
    __slots__ = ("_iterable", "_fn")

    def __init__(self, iterable: Iterable[T], fn: Callable[[T], U | None]) -> None:
        self._iterable = iterable
        self._fn = fn

    def __iter__(self) -> _FilterMapIterator[T, U]:
        return _FilterMapIterator(iter(self._iterable), self._fn)

    def __repr__(self) -> str:
        return "FilterMap(...)"


class _FlatMapIterator(Generic[T, U]):
    __slots__ = ("_iter", "_fn", "_current")

    def __init__(self, iterable: Iterator[T], fn: Callable[[T], Iterable[U]]) -> None:
        self._iter = iterable
        self._fn = fn
        self._current: Iterator[U] | None = None

    def __iter__(self) -> _FlatMapIterator[T, U]:
        return self

    def __next__(self) -> U:
        while True:
            if self._current is not None:
                try:
                    return next(self._current)
                except StopIteration:
                    self._current = None
            val = next(self._iter)
            self._current = iter(self._fn(val))


class FlatMap(Generic[T, U]):
    __slots__ = ("_iterable", "_fn")

    def __init__(self, iterable: Iterable[T], fn: Callable[[T], Iterable[U]]) -> None:
        self._iterable = iterable
        self._fn = fn

    def __iter__(self) -> _FlatMapIterator[T, U]:
        return _FlatMapIterator(iter(self._iterable), self._fn)

    def __repr__(self) -> str:
        return "FlatMap(...)"


class _FlattenIterator(Generic[T]):
    __slots__ = ("_iter", "_current")

    def __init__(self, iterable: Iterable[Iterable[T]]) -> None:
        self._iter = iter(iterable)
        self._current: Iterator[T] | None = None

    def __iter__(self) -> _FlattenIterator[T]:
        return self

    def __next__(self) -> T:
        while True:
            if self._current is not None:
                try:
                    return next(self._current)
                except StopIteration:
                    self._current = None
            inner = next(self._iter)
            self._current = iter(inner)


class Flatten(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[Iterable[T]]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _FlattenIterator[T]:
        return _FlattenIterator(self._iterable)

    def __repr__(self) -> str:
        return "Flatten(...)"


class _PeekableIterator(Generic[T]):
    __slots__ = ("_iter", "_peeked", "_has_peeked")

    def __init__(self, iterable: Iterator[T]) -> None:
        self._iter = iterable
        self._peeked: T | None = None
        self._has_peeked = False

    def __iter__(self) -> _PeekableIterator[T]:
        return self

    def __next__(self) -> T:
        if self._has_peeked:
            self._has_peeked = False
            return self._peeked  # type: ignore
        return next(self._iter)

    def peek(self) -> T | None:  # type: ignore
        if not self._has_peeked:
            try:
                self._peeked = next(self._iter)
                self._has_peeked = True
            except StopIteration:
                return None
        return self._peeked

    def peek_mut(self) -> PeekMut[T]:  # type: ignore
        if not self._has_peeked:
            try:
                self._peeked = next(self._iter)
                self._has_peeked = True
            except StopIteration:
                return PeekMut(None, False)
        return PeekMut(self._peeked, True)


class PeekMut(Generic[T]):
    __slots__ = ("_value", "_valid")

    def __init__(self, value: T | None, valid: bool) -> None:
        self._value = value
        self._valid = valid

    def __bool__(self) -> bool:
        return self._valid

    def __enter__(self) -> PeekMut:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __repr__(self) -> str:
        if self._valid:
            return f"Some({self._value!r})"
        return "None"


class Peekable(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _PeekableIterator[T]:
        return _PeekableIterator(iter(self._iterable))

    def __repr__(self) -> str:
        return "Peekable(...)"


class _FuseIterator(Generic[T]):
    __slots__ = ("_iter", "_exhausted")

    def __init__(self, iterable: Iterator[T]) -> None:
        self._iter = iterable
        self._exhausted = False

    def __iter__(self) -> _FuseIterator[T]:
        return self

    def __next__(self) -> T:
        if self._exhausted:
            raise StopIteration
        try:
            return next(self._iter)
        except StopIteration:
            self._exhausted = True
            raise

    def is_exhausted(self) -> bool:  # type: ignore
        return self._exhausted


class Fuse(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _FuseIterator[T]:
        return _FuseIterator(iter(self._iterable))

    def __repr__(self) -> str:
        return "Fuse(...)"


class _ChainIterator(Generic[T]):
    __slots__ = ("_iter_a", "_iter_b", "_first_done")

    def __init__(self, a: Iterator[T], b: Iterator[T]) -> None:
        self._iter_a = a
        self._iter_b = b
        self._first_done = False

    def __iter__(self) -> _ChainIterator[T]:
        return self

    def __next__(self) -> T:
        if not self._first_done:
            try:
                return next(self._iter_a)
            except StopIteration:
                self._first_done = True
        return next(self._iter_b)


class Chain(Generic[T]):
    __slots__ = ("_iter_a", "_iter_b")

    def __init__(self, a: Iterable[T], b: Iterable[T]) -> None:
        self._iter_a = a
        self._iter_b = b

    def __iter__(self) -> _ChainIterator[T]:
        return _ChainIterator(iter(self._iter_a), iter(self._iter_b))

    def __repr__(self) -> str:
        return "Chain(...)"


class _CycleIterator(Generic[T]):
    __slots__ = ("_original", "_iter", "_exhausted")

    def __init__(self, iterable: Iterable[T]) -> None:
        self._original = list(iterable)
        self._iter = iter(self._original)
        self._exhausted = False

    def __iter__(self) -> _CycleIterator[T]:
        return self

    def __next__(self) -> T:
        if self._exhausted:
            self._iter = iter(self._original)
            self._exhausted = False
        try:
            return next(self._iter)
        except StopIteration:
            self._exhausted = True
            self._iter = iter(self._original)
            return next(self._iter)


class Cycle(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _CycleIterator[T]:
        return _CycleIterator(self._iterable)

    def __repr__(self) -> str:
        return "Cycle(...)"


class _TakeIterator(Generic[T]):
    __slots__ = ("_iter", "_remaining")

    def __init__(self, iterable: Iterator[T], n: int) -> None:
        self._iter = iterable
        self._remaining = n

    def __iter__(self) -> _TakeIterator[T]:
        return self

    def __next__(self) -> T:
        if self._remaining <= 0:
            raise StopIteration
        self._remaining -= 1
        return next(self._iter)


class Take(Generic[T]):
    __slots__ = ("_iterable", "_n")

    def __init__(self, iterable: Iterable[T], n: int) -> None:
        self._iterable = iterable
        self._n = n

    def __iter__(self) -> _TakeIterator[T]:
        return _TakeIterator(iter(self._iterable), self._n)

    def __repr__(self) -> str:
        return "Take(...)"


class _SkipIterator(Generic[T]):
    __slots__ = ("_iter", "_remaining")

    def __init__(self, iterable: Iterable[T], n: int) -> None:
        self._iter = iter(iterable)
        self._remaining = n

    def __iter__(self) -> _SkipIterator[T]:
        return self

    def __next__(self) -> T:
        while self._remaining > 0:
            next(self._iter)
            self._remaining -= 1
        return next(self._iter)


class Skip(Generic[T]):
    __slots__ = ("_iterable", "_n")

    def __init__(self, iterable: Iterable[T], n: int) -> None:
        self._iterable = iterable
        self._n = n

    def __iter__(self) -> _SkipIterator[T]:
        return _SkipIterator(self._iterable, self._n)

    def __repr__(self) -> str:
        return "Skip(...)"


class _RevIterator(Generic[T]):
    __slots__ = ("_buffer", "_index")

    def __init__(self, iterable: Iterable[T]) -> None:
        self._buffer = list(iterable)
        self._index = len(self._buffer) - 1

    def __iter__(self) -> _RevIterator[T]:
        return self

    def __next__(self) -> T:
        if self._index < 0:
            raise StopIteration
        val = self._buffer[self._index]
        self._index -= 1
        return val


class Rev(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _RevIterator[T]:
        return _RevIterator(self._iterable)

    def __repr__(self) -> str:
        return "Rev(...)"


class _InspectIterator(Generic[T]):
    __slots__ = ("_iter", "_fn")

    def __init__(self, iterable: Iterator[T], fn: Callable[[T], Any]) -> None:
        self._iter = iterable
        self._fn = fn

    def __iter__(self) -> _InspectIterator[T]:
        return self

    def __next__(self) -> T:
        val = next(self._iter)
        self._fn(val)
        return val


class Inspect(Generic[T]):
    __slots__ = ("_iterable", "_fn")

    def __init__(self, iterable: Iterable[T], fn: Callable[[T], Any]) -> None:
        self._iterable = iterable
        self._fn = fn

    def __iter__(self) -> _InspectIterator[T]:
        return _InspectIterator(iter(self._iterable), self._fn)

    def __repr__(self) -> str:
        return "Inspect(...)"


class _CopiedIterator(Generic[T]):
    __slots__ = ("_iter",)

    def __init__(self, iterable: Iterator[T]) -> None:
        self._iter = iterable

    def __iter__(self) -> _CopiedIterator[T]:
        return self

    def __next__(self) -> T:
        return next(self._iter)


class Copied(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _CopiedIterator[T]:
        return _CopiedIterator(iter(self._iterable))

    def __repr__(self) -> str:
        return "Copied(...)"


class Cloned(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _CopiedIterator[T]:
        return _CopiedIterator(iter(self._iterable))

    def __repr__(self) -> str:
        return "Cloned(...)"


class _PartitionIterator(Generic[T]):
    __slots__ = ("_iter", "_pred", "_true_buf", "_false_buf", "_true_idx", "_false_idx")

    def __init__(self, iterable: Iterator[T], pred: Callable[[T], bool]) -> None:
        items = list(iterable)
        self._true_buf = [item for item in items if pred(item)]
        self._false_buf = [item for item in items if not pred(item)]
        self._true_idx = 0
        self._false_idx = 0

    def __iter__(self) -> _PartitionIterator[T]:
        return self

    def __next__(self) -> tuple[list[T], list[T]]:
        if self._true_idx == 0 and self._false_idx == 0:
            self._true_idx = 1
            return (self._true_buf, self._false_buf)
        raise StopIteration


class Partition(Generic[T]):
    __slots__ = ("_iterable", "_pred")

    def __init__(self, iterable: Iterable[T], pred: Callable[[T], bool]) -> None:
        self._iterable = iterable
        self._pred = pred

    def collect(self) -> tuple[list[T], list[T]]:  # type: ignore
        true_list = []
        false_list = []
        for item in self._iterable:
            if self._pred(item):
                true_list.append(item)
            else:
                false_list.append(item)
        return (true_list, false_list)

    def __repr__(self) -> str:
        return "Partition(...)"
