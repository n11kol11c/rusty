"""Debugging utilities — dbg, format_, cfg, matches, include_str, include_bytes."""
from __future__ import annotations

"""Debugging utilities — formatting, inspection, and configuration.

Provides Formatter, format_, write_, writeln_, dbg_, dbg, cfg,
option_env, include_str, include_bytes, and matches.
"""

import inspect
import os
import traceback
from typing import Any


class Formatter:
    __slots__ = ("_buf",)

    def __init__(self) -> None:
        self._buf: list[str] = []

    def write_str(self, s: str) -> None:  # type: ignore
        self._buf.append(s)

    def write_char(self, c: str) -> None:  # type: ignore
        self._buf.append(c)

    def write_fmt(self, args: str) -> None:  # type: ignore
        self._buf.append(args)

    def finish(self) -> str:  # type: ignore
        return "".join(self._buf)

    def as_str(self) -> str:  # type: ignore
        return "".join(self._buf)

    def __str__(self) -> str:
        return "".join(self._buf)


def format_(template: str, *args: Any, **kwargs: Any) -> str:
    return template.format(*args, **kwargs)


def write_(buf: Any, template: str, *args: Any, **kwargs: Any) -> None:
    formatted = template.format(*args, **kwargs)
    if hasattr(buf, 'write'):
        buf.write(formatted)
    elif hasattr(buf, 'append'):
        buf.append(formatted)


def writeln_(buf: Any, template: str = "", *args: Any, **kwargs: Any) -> None:
    formatted = template.format(*args, **kwargs) if template else ""
    if hasattr(buf, 'write'):
        buf.write(formatted + "\n")
    elif hasattr(buf, 'append'):
        buf.append(formatted + "\n")


def dbg_(*args: Any) -> Any:
    frames = traceback.extract_stack()
    if len(frames) >= 2:
        frame = frames[-2]
        loc = f"{frame.filename}:{frame.lineno}"
    else:
        loc = "<unknown>"
    parts = []
    for i, arg in enumerate(args):
        parts.append(f"{arg!r}")
    print(f"[{loc}] {', '.join(parts)}")
    return args[0] if len(args) == 1 else args


def dbg(value: Any, *args: Any, **kwargs: Any) -> Any:
    frame = inspect.currentframe()
    caller = frame.f_back if frame else None  # type: ignore
    var_name = ""
    if caller:
        code = caller.f_code
        for name in code.co_varnames:
            if caller.f_locals.get(name) is value:
                var_name = name
                break
    loc = ""
    if caller:
        loc = f"{caller.f_code.co_filename}:{caller.f_lineno}"
    prefix = f"[{var_name}]" if var_name else ""
    suffix = ""
    if args:
        suffix = " " + " ".join(str(a) for a in args)
    if kwargs:
        suffix += " " + " ".join(f"{k}={v!r}" for k, v in kwargs.items())
    print(f"{prefix} {value!r}{suffix} @ {loc}")
    return value


def cfg(key: str, default: str = "") -> str:
    return os.environ.get(f"CFG_{key.upper()}", default)


def compile_error(message: str) -> None:
    raise SyntaxError(f"compile_error: {message}")


def option_env(key: str) -> str | None:
    return os.environ.get(key)


def include_str(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


def include_bytes(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()


def matches(value: Any, pattern: Any) -> bool:
    if callable(pattern):
        return pattern(value)
    return value == pattern
