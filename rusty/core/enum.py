"""Enum and Variant — tagged unions with match() pattern matching."""
from __future__ import annotations

"""Enum type — tagged unions with pattern matching.

Provides Enum, Variant for building algebraic data types, and the match()
function for exhaustive pattern matching with wildcard support.
"""

from typing import Any, Callable, Generic, Iterable, Iterator, TypeVar


T = TypeVar("T")
R = TypeVar("R")


class MatchError(Exception):
    pass


class _Case(Generic[T, R]):
    __slots__ = ("pattern", "handler", "guard")

    def __init__(
        self,
        pattern: T | type | tuple[type, ...] | None,
        handler: Callable[[T], R] | R,
        guard: Callable[[T], bool] | None,
    ) -> None:
        self.pattern = pattern
        self.handler = handler
        self.guard = guard

    def matches(self, value: object) -> bool:
        if self.pattern is _:
            return True
        if self.pattern is None:
            return value is None
        if isinstance(self.pattern, type):
            if not isinstance(value, self.pattern):
                return False
        elif isinstance(self.pattern, tuple):
            if not isinstance(value, self.pattern):
                return False
        elif self.pattern != value:
            return False
        if self.guard is not None and not self.guard(value):
            return False
        return True

    def execute(self, value: T) -> R:
        if callable(self.handler) and not isinstance(self.handler, type):
            return self.handler(value)
        return self.handler  # type: ignore[return-value]


class Match(Generic[T, R]):
    __slots__ = ("_value", "_cases", "_executed", "_result")

    def __init__(self, value: T) -> None:
        self._value = value
        self._cases: list[_Case] = []
        self._executed = False
        self._result: R = None  # type: ignore[assignment]

    def case(
        self,
        pattern: object | type | tuple[type, ...] | None,
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        self._cases.append(_Case(pattern, handler, guard))
        return self

    def case_type(
        self,
        typ: type | tuple[type, ...],
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        self._cases.append(_Case(typ, handler, guard))
        return self

    def case_eq(
        self,
        value: object,
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        self._cases.append(_Case(value, handler, guard))
        return self

    def case_range(
        self,
        start: int,
        end: int,
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        class _RangePattern:
            def __init__(self, s: int, e: int) -> None:
                self.start = s
                self.end = e
            def __eq__(self, other: object) -> bool:
                if isinstance(other, (int, float)):
                    return self.start <= other < self.end
                return NotImplemented
        self._cases.append(_Case(_RangePattern(start, end), handler, guard))
        return self

    def case_pred(
        self,
        predicate: Callable[[T], bool],
        handler: Callable[[T], R] | R | None = None,
    ) -> Match[T, R]:
        class _PredPattern:
            def __init__(self, pred: Callable[[T], bool]) -> None:
                self.pred = pred
            def __eq__(self, other: object) -> bool:
                return self.pred(other)  # type: ignore[arg-type]
        self._cases.append(_Case(_PredPattern(predicate), handler, None))
        return self

    def case_in(
        self,
        collection: Iterable[object],
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        class _InPattern:
            def __init__(self, coll: Iterable[object]) -> None:
                self.coll = coll
            def __eq__(self, other: object) -> bool:
                return other in self.coll
        self._cases.append(_Case(_InPattern(collection), handler, guard))
        return self

    def otherwise(self, handler: Callable[[T], R] | R) -> R:
        self._cases.append(_Case(_, handler, None))
        return self.execute()

    def execute(self) -> R:
        if self._executed:
            return self._result
        for case in self._cases:
            if case.matches(self._value):
                self._result = case.execute(self._value)
                self._executed = True
                return self._result
        raise MatchError(
            f"no match found for {self._value!r}"
        )

    def __repr__(self) -> str:
        if self._executed:
            return f"Match({self._value!r} => {self._result!r})"
        return f"Match({self._value!r}, {len(self._cases)} cases)"


class _MatchWildcard:
    __slots__ = ()

    def __eq__(self, other: object) -> bool:
        return True

    def __hash__(self) -> int:
        return hash("_")

    def __repr__(self) -> str:
        return "_"


class _:
    __slots__ = ()

    def __eq__(self, other: object) -> bool:
        return True

    def __hash__(self) -> int:
        return hash("_")

    def __repr__(self) -> str:
        return "_"


_ = _MatchWildcard()


def match(value: T) -> Match[T, Any]:
    return Match(value)


class Variant:
    __slots__ = ("_tag", "_value", "_enum_cls")

    def __init__(self, tag: str, value: Any, enum_cls: type | None = None) -> None:
        self._tag = tag
        self._value = value
        self._enum_cls = enum_cls

    @property
    def tag(self) -> str:
        return self._tag

    @property
    def value(self) -> Any:
        return self._value

    def is_(self, *tags: str) -> bool:
        return self._tag in tags

    def unwrap(self) -> Any:
        return self._value

    def unwrap_or(self, default: Any) -> Any:
        return self._value

    def expect(self, message: str) -> Any:
        return self._value

    def map(self, fn: Callable[[Any], Any]) -> Variant:
        return Variant(self._tag, fn(self._value), self._enum_cls)

    def map_or(self, default: Any, fn: Callable[[Any], Any]) -> Any:
        return fn(self._value)

    def and_then(self, fn: Callable[[Any], Variant]) -> Variant:
        return fn(self._value)

    def or_else(self, fn: Callable[[str], Variant]) -> Variant:
        return self

    def match(self, *cases: tuple[str, Callable[[Any], Any]]) -> Any:
        for case in cases:
            pattern, handler = case[0], case[1]
            if isinstance(pattern, _MatchWildcard):
                return handler(self._value)
            if isinstance(pattern, tuple) and len(pattern) == 2:
                t, guard = pattern
                if t == self._tag and guard(self._value):
                    return handler(self._value)
            elif pattern == self._tag:
                return handler(self._value)
        raise MatchError(f"no match for {self!r}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Variant):
            return self._tag == other._tag and self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._tag, self._value))

    def __repr__(self) -> str:
        if self._value is None:
            return self._tag
        return f"{self._tag}({self._value!r})"


class _EnumMeta(type):
    def __new__(cls, name, bases, namespace) -> type:
        variants = {}
        for key, val in list(namespace.items()):
            if key.startswith("_") or callable(val):
                continue
            if isinstance(val, tuple) and len(val) >= 1 and isinstance(val[0], str):
                variants[val[0]] = val[1:]
            elif isinstance(val, str):
                variants[val] = ()
        namespace["_variants"] = variants
        for key in list(variants.keys()):
            if key in namespace:
                del namespace[key]
        obj = super().__new__(cls, name, bases, namespace)
        return obj

    def __getattr__(cls, name: str) -> Variant:
        if name.startswith("_"):
            raise AttributeError(name)
        variants = cls.__dict__.get("_variants", {})
        if name in variants:
            val = variants[name]
            return Variant(name, val[0] if len(val) == 1 else val, cls)
        raise AttributeError(f"enum {cls.__name__} has no variant '{name}'")


class Enum(metaclass=_EnumMeta):
    @classmethod
    def variants(cls) -> list[str]:
        return list(cls._variants.keys())  # type: ignore

    @classmethod
    def is_valid(cls, tag: str) -> bool:
        return tag in cls._variants  # type: ignore

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.__dict__})"
