"""Result type — Ok(value) or Err(error) with ? propagation via propagate/ask."""
from __future__ import annotations

"""Result type — a container for success or failure.

Provides Result, Ok, Err for explicit error handling. Supports the ? operator
via propagate/ask for clean error propagation through call chains.
"""

from dataclasses import dataclass
from typing import Any, Callable, Generic, NoReturn, TypeVar

from .option import Option, Some, None_


T = TypeVar("T")
E = TypeVar("E", bound=BaseException)
U = TypeVar("U")
F = TypeVar("F", bound=Callable[..., Any])


class Result(Generic[T, E]):
    def is_ok(self) -> bool:
        return isinstance(self, Ok)

    def is_err(self) -> bool:
        return isinstance(self, Err)

    def unwrap(self) -> T:
        if isinstance(self, Ok):
            return self.value

        raise RuntimeError(
            "called `Result.unwrap()` on an `Err` value: "
            f"{self.error!r}"
        )

    def expect(self, message: str) -> T:
        if isinstance(self, Ok):
            return self.value
        raise RuntimeError(
            f"{message}: {self.error!r}"
        )

    def unwrap_err(self) -> E:
        if isinstance(self, Err):
            return self.error
        raise RuntimeError(
            "called `Result.unwrap_err()` on an `Ok` value: "
            f"{self.value!r}"
        )

    def expect_err(self, message: str) -> E:
        if isinstance(self, Err):
            return self.error
        raise RuntimeError(
            f"{message}: {self.value!r}"
        )

    def unwrap_or(self, default: T) -> T:
        if isinstance(self, Ok):
            return self.value
        return default

    def unwrap_or_else(
        self,
        fn: Callable[[E], T],
    ) -> T:
        if isinstance(self, Ok):
            return self.value
        return fn(self.error)

    def map(
        self,
        fn: Callable[[T], U],
    ) -> Result[U, E]:
        if isinstance(self, Ok):
            return Ok(fn(self.value))
        return self

    def map_err(
        self,
        fn: Callable[[E], U],
    ) -> Result[T, U]:
        if isinstance(self, Err):
            return Err(fn(self.error))
        return self

    def map_or(
        self,
        default: U,
        fn: Callable[[T], U],
    ) -> U:
        if isinstance(self, Ok):
            return fn(self.value)
        return default

    def map_or_else(
        self,
        default: Callable[[E], U],
        fn: Callable[[T], U],
    ) -> U:
        if isinstance(self, Ok):
            return fn(self.value)
        return default(self.error)

    def and_(
        self,
        other: Result[U, E],
    ) -> Result[U, E]:
        if isinstance(self, Ok):
            return other
        return self

    def and_then(
        self,
        fn: Callable[[T], Result[U, E]],
    ) -> Result[U, E]:
        if isinstance(self, Ok):
            return fn(self.value)
        return self

    def or_(
        self,
        other: Result[T, U],
    ) -> Result[T, U]:
        if isinstance(self, Ok):
            return self
        return other

    def or_else(
        self,
        fn: Callable[[E], Result[T, U]],
    ) -> Result[T, U]:
        if isinstance(self, Err):
            return fn(self.error)
        return self

    def ok(self) -> Option[T]:
        if isinstance(self, Ok):
            return Some(self.value)
        return None_

    def err(self) -> Option[E]:
        if isinstance(self, Err):
            return Some(self.error)
        return None_

    def inspect(
        self,
        fn: Callable[[T], Any],
    ) -> Result[T, E]:
        if isinstance(self, Ok):
            fn(self.value)
        return self

    def inspect_err(
        self,
        fn: Callable[[E], Any],
    ) -> Result[T, E]:
        if isinstance(self, Err):
            fn(self.error)
        return self

    def __bool__(self) -> bool:
        return self.is_ok()

    def __repr__(self) -> str:
        if isinstance(self, Ok):
            return f"Ok({self.value!r})"
        return f"Err({self.error!r})"


@dataclass(frozen=True, slots=True)
class Ok(Result[T, NoReturn]):
    value: T

@dataclass(frozen=True, slots=True)
class Err(Result[NoReturn, E]):
    error: E


class PropagateError(Exception):
    __slots__ = ("_result",)

    def __init__(self, result: Result) -> None:
        self._result = result

    @property
    def result(self) -> Result:
        return self._result


class Propagate:
    __slots__ = ("_fn",)

    def __init__(self, fn: F) -> None:
        self._fn = fn

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return self._fn(*args, **kwargs)
        except PropagateError as e:
            return e.result

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        return Propagate(lambda *a, **kw: self._fn(obj, *a, **kw))


def propagate(fn: F) -> F:
    return Propagate(fn)  # type: ignore[return-value]


def ask(result: Result) -> Any:
    if isinstance(result, Err):
        raise PropagateError(result)
    return result.value


def try_ask(fn: F) -> F:
    def wrapper(*args: Any, **kwargs: Any) -> Result:
        try:
            return Ok(fn(*args, **kwargs))
        except Exception as e:
            return Err(e)
    return wrapper  # type: ignore[return-value]
