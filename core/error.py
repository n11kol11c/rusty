"""Error infrastructure — Error, Backtrace, Location, and context() for error chaining."""
from __future__ import annotations

"""Error infrastructure — structured error handling.

Provides Error, Backtrace, Location, and context() for building rich
error chains with source tracking and stack trace capture.
"""

import traceback


class Location:
    __slots__ = ("_file", "_line", "_column")

    def __init__(self, file: str = "", line: int = 0, column: int = 0) -> None:
        self._file = file
        self._line = line
        self._column = column

    def file(self) -> str:  # type: ignore
        return self._file

    def line(self) -> int:  # type: ignore
        return self._line

    def column(self) -> int:  # type: ignore
        return self._column

    def __str__(self) -> str:
        return f"{self._file}:{self._line}:{self._column}"

    def __repr__(self) -> str:
        return f"Location({self._file!r}, {self._line}, {self._column})"


class Backtrace:
    __slots__ = ("_frames", "_formatted")

    def __init__(self) -> None:
        self._frames = traceback.extract_stack()
        self._formatted = "".join(traceback.format_stack())

    def __str__(self) -> str:
        return self._formatted

    def __repr__(self) -> str:
        return f"Backtrace({len(self._frames)} frames)"

    def frames(self) -> list:  # type: ignore
        return self._frames


class Error(Exception):
    __slots__ = ("_message", "_source", "_backtrace", "_location", "_context")

    def __init__(self, message: str = "", source: Exception | None = None) -> None:
        super().__init__(message)
        self._message = message
        self._source = source
        self._backtrace: Backtrace | None = None
        self._location: Location | None = None
        self._context: str | None = None

    @classmethod
    def new(cls, message: str) -> Error:  # type: ignore
        return cls(message)

    @classmethod
    def from_source(cls, source: Exception) -> Error:  # type: ignore
        return cls(str(source), source)

    def message(self) -> str:  # type: ignore
        return self._message

    def source(self) -> Exception | None:  # type: ignore
        return self._source

    def backtrace(self) -> Backtrace:  # type: ignore
        if self._backtrace is None:
            self._backtrace = Backtrace()
        return self._backtrace

    def location(self) -> Location | None:  # type: ignore
        return self._location

    def with_context(self, ctx: str) -> Error:  # type: ignore
        self._context = ctx
        return self

    def context(self) -> str | None:  # type: ignore
        return self._context

    def with_source(self, source: Exception) -> Error:  # type: ignore
        self._source = source
        return self

    def __str__(self) -> str:
        parts = [self._message]
        if self._context:
            parts.append(f"context: {self._context}")
        if self._source:
            parts.append(f"source: {self._source}")
        return ": ".join(parts)


def context(msg: str, err: Exception) -> Error:
    e = Error(msg)
    e._source = err
    e._context = msg
    e._backtrace = Backtrace()
    return e
