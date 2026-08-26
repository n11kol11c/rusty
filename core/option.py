"""Option type — Some(value) or None_ for explicit null handling."""
from __future__ import annotations

"""Option type — a container for an optional value.

Provides Option, Some, None_ for explicit null handling without None confusion.
Every Option is either Some(value) or None_, forcing callers to handle both cases.
"""

from dataclasses import dataclass
from typing import Any, Callable, Generic, NoReturn, TypeVar


T = TypeVar("T")
U = TypeVar("U")


class Option(Generic[T]):
    def is_some(self) -> bool:
        return isinstance(self, Some)

    def is_none(self) -> bool:
        return isinstance(self, NoneOption)

    def unwrap(self) -> T:
        if isinstance(self, Some):
            return self.value
        raise RuntimeError(
            "called `Option.unwrap()` on a `None` value"
        )

    def expect(self, message: str) -> T:
        if isinstance(self, Some):
            return self.value
        raise RuntimeError(message)

    def unwrap_or(self, default: T) -> T:
        if isinstance(self, Some):
            return self.value
        return default

    def unwrap_or_else(
        self,
        fn: Callable[[], T],
    ) -> T:
        if isinstance(self, Some):
            return self.value
        return fn()

    def map(
        self,
        fn: Callable[[T], U],
    ) -> Option[U]:
        if isinstance(self, Some):
            return Some(fn(self.value))
        return None_

    def map_or(
        self,
        default: U,
        fn: Callable[[T], U],
    ) -> U:
        if isinstance(self, Some):
            return fn(self.value)
        return default

    def map_or_else(
        self,
        default: Callable[[], U],
        fn: Callable[[T], U],
    ) -> U:
        if isinstance(self, Some):
            return fn(self.value)
        return default()

    def and_(
        self,
        other: Option[U],
    ) -> Option[U]:
        if isinstance(self, Some):
            return other
        return None_

    def and_then(
        self,
        fn: Callable[[T], Option[U]],
    ) -> Option[U]:
        if isinstance(self, Some):
            return fn(self.value)
        return None_

    def or_(
        self,
        other: Option[T],
    ) -> Option[T]:
        if isinstance(self, Some):
            return self
        return other

    def or_else(
        self,
        fn: Callable[[], Option[T]],
    ) -> Option[T]:
        if isinstance(self, Some):
            return self
        return fn()

    def filter(
        self,
        predicate: Callable[[T], bool],
    ) -> Option[T]:
        if isinstance(self, Some):
            if predicate(self.value):
                return self
        return None_

    def inspect(
        self,
        fn: Callable[[T], Any],
    ) -> Option[T]:
        if isinstance(self, Some):
            fn(self.value)
        return self

    def __bool__(self) -> bool:
        return self.is_some()

    def __iter__(self):
        if isinstance(self, Some):
            yield self.value

    def __repr__(self) -> str:
        if isinstance(self, Some):
            return f"Some({self.value!r})"
        return "None"


@dataclass(frozen=True, slots=True)
class Some(Option[T]):
    value: T


class NoneOption(Option[NoReturn]):
    __slots__ = ()
    _instance: NoneOption | None = None

    def __new__(cls) -> NoneOption:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

None_ = NoneOption()
none = None_
