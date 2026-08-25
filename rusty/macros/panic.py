"""Panic helpers — panic, todo, unimplemented, ScopeGuard, defer."""
from __future__ import annotations

"""Panic and error utilities — abort, todo, and resource management.

Provides panic, todo, unimplemented for intentional crashes,
ScopeGuard and defer for RAII-style cleanup.
"""

import traceback
from typing import Any, Callable, Generic, TypeVar, NoReturn

T = TypeVar("T")


class UnimplementedError(Exception):
    __slots__ = ("_message",)

    def __init__(self, message: str | None = None) -> None:
        self._message = message or "not yet implemented"
        super().__init__(self._message)


def unimplemented(message: str | None = None) -> NoReturn:
    raise UnimplementedError(message)


def todo(message: str | None = None) -> NoReturn:
    raise UnimplementedError(message or "not yet implemented")


class PanicError(Exception):
    __slots__ = ("_message", "_backtrace")

    def __init__(self, message: str | None = None) -> None:
        self._message = message or "explicit panic"
        self._backtrace = traceback.format_stack()
        super().__init__(self._message)

    @property
    def backtrace(self) -> list[str]:
        return self._backtrace

    def __str__(self) -> str:
        tb = "".join(self._backtrace[:-1])
        return f"panicked at '{self._message}'\n{tb}"


def panic(message: str | None = None) -> NoReturn:
    raise PanicError(message)


def panic_fmt(*args: Any, **kwargs: Any) -> NoReturn:
    msg = " ".join(str(a) for a in args)
    for k, v in kwargs.items():
        msg += f" {k}={v!r}"
    raise PanicError(msg)


class ScopeGuard(Generic[T]):
    __slots__ = ("_fn", "_cancelled", "_value")

    def __init__(self, fn: Callable[[], T], value: T | None = None) -> None:
        self._fn = fn
        self._cancelled = False
        self._value = value

    def cancel(self) -> None:
        self._cancelled = True

    def is_cancelled(self) -> bool:
        return self._cancelled

    def execute(self) -> T | None:
        if not self._cancelled:
            self._cancelled = True
            return self._fn()
        return None

    def __enter__(self) -> ScopeGuard[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        if not self._cancelled:
            self._cancelled = True
            self._fn()

    def __repr__(self) -> str:
        return f"ScopeGuard(cancelled={self._cancelled})"


def defer(fn: Callable[[], Any]) -> ScopeGuard:
    return ScopeGuard(fn)
