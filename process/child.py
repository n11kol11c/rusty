"""Child and Stdio — running process handles and stream config."""
from __future__ import annotations

"""Child and Stdio — running process handles.

Provides Child for managing running processes and Stdio for
configuring process standard streams.
"""

from typing import Any

from .output import ExitStatus, Output
from ..fs.path import Path


class Stdio:
    __slots__ = ("_kind", "_file")

    INHERIT = 0
    PIPED = 1
    NULL = 2
    FILE = 3

    def __init__(self, kind: int = INHERIT, file: str | None = None) -> None:
        self._kind = kind
        self._file = file

    @classmethod
    def inherit(cls) -> Stdio:
        return cls(cls.INHERIT)

    @classmethod
    def piped(cls) -> Stdio:
        return cls(cls.PIPED)

    @classmethod
    def null(cls) -> Stdio:
        return cls(cls.NULL)

    @classmethod
    def from_path(cls, path: str | Path) -> Stdio:  # type: ignore
        path_str = path.as_str() if isinstance(path, Path) else str(path)
        return cls(cls.FILE, path_str)

    def kind(self) -> int:
        return self._kind

    def __repr__(self) -> str:
        if self._kind == self.INHERIT:
            return "Stdio::Inherit"
        if self._kind == self.PIPED:
            return "Stdio::Piped"
        if self._kind == self.NULL:
            return "Stdio::Null"
        return f"Stdio::File({self._file!r})"


class Child:
    __slots__ = ("_process", "_pid")

    def __init__(self, process: Any) -> None:
        self._process = process
        self._pid = process.pid

    def id(self) -> int:  # type: ignore
        return self._pid

    def kill(self) -> None:  # type: ignore
        self._process.kill()

    def wait(self) -> ExitStatus:  # type: ignore
        code = self._process.wait()
        return ExitStatus(code)

    def wait_with_output(self) -> Output:  # type: ignore
        stdout, stderr = self._process.communicate()
        return Output(
            ExitStatus(self._process.returncode),
            stdout or b"",
            stderr or b"",
        )

    def try_wait(self) -> ExitStatus | None:  # type: ignore
        ret = self._process.poll()
        if ret is None:
            return None
        return ExitStatus(ret)

    def take_stdin(self) -> Any:  # type: ignore
        return self._process.stdin

    def take_stdout(self) -> Any:  # type: ignore
        return self._process.stdout

    def take_stderr(self) -> Any:  # type: ignore
        return self._process.stderr

    def wait_timeout(self, secs: float) -> ExitStatus | None:  # type: ignore
        ret = self._process.poll()
        if ret is not None:
            return ExitStatus(ret)
        try:
            self._process.wait(timeout=secs)
            return ExitStatus(self._process.returncode)
        except Exception:
            return None

    def __repr__(self) -> str:
        return f"Child(pid={self._pid})"
