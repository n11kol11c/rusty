"""Iterator consumers — collect, fold, count, sum, min, max, any, all, find."""
from __future__ import annotations

"""Iterator consumers — consume iterators into values.

Provides standalone functions: collect, fold, for_each, count, sum, min,
max, any, all, find, position, and more for consuming iterator results.
"""

from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    TypeVar,
)

from .adapters import (
    Chain,
    Cloned,
    Copied,
    Cycle,
    Enumerate,
    Filter,
    FilterMap,
    FlatMap,
    Flatten,
    Inspect,
    Map,
    Peekable,
    Rev,
    Skip,
    Take,
    Zip,
)
from .iterator import Iter, PeekableIter

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


def collect(iterable: Iterable[T]) -> list[T]:
    return list(iterable)


def fold(iterable: Iterable[T], init: U, fn: Callable[[U, T], U]) -> U:
    acc = init
    for v in iterable:
        acc = fn(acc, v)
    return acc


def for_each(iterable: Iterable[T], fn: Callable[[T], Any]) -> None:
    for v in iterable:
        fn(v)


def count(iterable: Iterable[T]) -> int:
    n = 0
    for _ in iterable:
        n += 1
    return n


def sum(iterable: Iterable[T]) -> T:
    return fold(iterable, 0, lambda a, b: a + b)  # type: ignore


def min(iterable: Iterable[T]) -> T | None:
    it = iter(iterable)
    try:
        acc = next(it)
    except StopIteration:
        return None
    for v in it:
        if v < acc:
            acc = v
    return acc


def max(iterable: Iterable[T]) -> T | None:
    it = iter(iterable)
    try:
        acc = next(it)
    except StopIteration:
        return None
    for v in it:
        if v > acc:
            acc = v
    return acc


def any(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    for v in iterable:
        if predicate(v):
            return True
    return False


def all(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    for v in iterable:
        if not predicate(v):
            return False
    return True


def find(iterable: Iterable[T], predicate: Callable[[T], bool]) -> T | None:
    for v in iterable:
        if predicate(v):
            return v
    return None


def position(iterable: Iterable[T], predicate: Callable[[T], bool]) -> int | None:
    for i, v in enumerate(iterable):
        if predicate(v):
            return i
    return None


def zip(a: Iterable[T], b: Iterable[U]) -> Zip[T, U]:
    return Zip(a, b)


def enumerate(iterable: Iterable[T], start: int = 0) -> Enumerate[T]:
    return Enumerate(iterable, start)


def chain(a: Iterable[T], b: Iterable[T]) -> Chain[T]:
    return Chain(a, b)


def peek(iterable: Iterable[T]) -> Peekable[T]:
    return Peekable(iterable)


def step_by(iterable: Iterable[T], step: int) -> Iter[T]:
    return Iter(iterable).step_by(step)


def skip(iterable: Iterable[T], n: int) -> Skip[T]:
    return Skip(iterable, n)


def take(iterable: Iterable[T], n: int) -> Take[T]:
    return Take(iterable, n)


def rev(iterable: Iterable[T]) -> Rev[T]:
    return Rev(iterable)


def inspect(iterable: Iterable[T], fn: Callable[[T], Any]) -> Inspect[T]:
    return Inspect(iterable, fn)


def copied(iterable: Iterable[T]) -> Copied[T]:
    return Copied(iterable)


def cloned(iterable: Iterable[T]) -> Cloned[T]:
    return Cloned(iterable)


def filter(iterable: Iterable[T], predicate: Callable[[T], bool]) -> Filter[T]:
    return Filter(iterable, predicate)


def filter_map(iterable: Iterable[T], fn: Callable[[T], U | None]) -> FilterMap[T, U]:
    return FilterMap(iterable, fn)


def flat_map(iterable: Iterable[T], fn: Callable[[T], Iterable[U]]) -> FlatMap[T, U]:
    return FlatMap(iterable, fn)


def flatten(iterable: Iterable[Iterable[T]]) -> Flatten[T]:
    return Flatten(iterable)


def map(iterable: Iterable[T], fn: Callable[[T], U]) -> Map[T, U]:
    return Map(iterable, fn)
