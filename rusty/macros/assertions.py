"""Assertion macros — assert_eq, assert_ne, debug_assert, and variants."""
from __future__ import annotations

"""Assertion macros — debug and release assertions.

Provides assert_eq, assert_ne, assert_, debug_assert, debug_assert_eq,
debug_assert_ne for runtime correctness checks.
"""

import re
from typing import Any


class AssertionError(Exception):
    pass


def assert_(condition: bool, message: str = "assertion failed") -> None:
    if not condition:
        raise AssertionError(message)


def assert_eq(a: Any, b: Any, message: str | None = None) -> None:
    if a != b:
        msg = message or f"assertion failed: {a!r} != {b!r}"
        raise AssertionError(msg)


def assert_ne(a: Any, b: Any, message: str | None = None) -> None:
    if a == b:
        msg = message or f"assertion failed: {a!r} == {b!r}"
        raise AssertionError(msg)


def assert_matches(value: Any, pattern: str, message: str | None = None) -> None:
    if not re.match(pattern, str(value)):
        msg = message or f"assertion failed: {value!r} does not match {pattern!r}"
        raise AssertionError(msg)


def assert_type(value: Any, expected: type, message: str | None = None) -> None:
    if not isinstance(value, expected):
        msg = message or f"assertion failed: expected {expected.__name__}, got {type(value).__name__}"
        raise AssertionError(msg)


def debug_assert(condition: bool, message: str = "") -> None:
    if __debug__:
        assert condition, message


def debug_assert_eq(a: Any, b: Any, message: str = "") -> None:
    if __debug__:
        assert_eq(a, b, message)


def debug_assert_ne(a: Any, b: Any, message: str = "") -> None:
    if __debug__:
        assert_ne(a, b, message)
