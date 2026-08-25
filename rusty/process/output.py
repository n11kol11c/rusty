"""ExitStatus, Output, ExitCode, and OS functions (args, env, temp_dir, etc.)."""
from __future__ import annotations

"""Process output and OS utilities.

Provides ExitStatus, Output, ExitCode, and functions: args, env,
current_dir, current_exe, home_dir, temp_dir.
"""

import os
import sys
import tempfile
from typing import Any, Iterable

from ..fs.path import Path


class ExitCode:
    __slots__ = ("_code",)

    def __init__(self, code: int = 0) -> None:
        self._code = code

    @classmethod
    def success(cls) -> ExitCode:
        return cls(0)

    @classmethod
    def from_raw(cls, code: int) -> ExitCode:  # type: ignore
        return cls(code)

    def code(self) -> int:  # type: ignore
        return self._code

    def is_success(self) -> bool:
        return self._code == 0

    def __repr__(self) -> str:
        return f"ExitCode({self._code})"


class ExitStatus:
    __slots__ = ("_code", "_success")

    def __init__(self, code: int) -> None:
        self._code = code
        self._success = code == 0

    def code(self) -> int:  # type: ignore
        return self._code

    def success(self) -> bool:  # type: ignore
        return self._success

    def signal(self) -> int | None:  # type: ignore
        if self._code < 0:
            return -self._code
        return None

    def __repr__(self) -> str:
        return f"ExitStatus(code={self._code})"

    def __bool__(self) -> bool:
        return self._success


class Output:
    __slots__ = ("_status", "_stdout", "_stderr")

    def __init__(self, status: ExitStatus, stdout: bytes = b"", stderr: bytes = b"") -> None:
        self._status = status
        self._stdout = stdout
        self._stderr = stderr

    def status(self) -> ExitStatus:  # type: ignore
        return self._status

    def stdout(self) -> bytes:  # type: ignore
        return self._stdout

    def stderr(self) -> bytes:  # type: ignore
        return self._stderr

    def stdout_str(self) -> str:  # type: ignore
        return self._stdout.decode("utf-8", errors="replace")

    def stderr_str(self) -> str:  # type: ignore
        return self._stderr.decode("utf-8", errors="replace")

    def __repr__(self) -> str:
        return f"Output(status={self._status})"


def args() -> list[str]:  # type: ignore
    return sys.argv[1:]


def env(key: str, default: str | None = None) -> str | None:  # type: ignore
    return os.environ.get(key, default)


def current_dir() -> Path:  # type: ignore
    return Path(os.getcwd())


def current_exe() -> Path:  # type: ignore
    return Path(os.path.realpath(sys.argv[0]))


def home_dir() -> Path | None:  # type: ignore
    home = os.path.expanduser("~")
    if home:
        return Path(home)
    return None


def temp_dir() -> Path:  # type: ignore
    return Path(tempfile.gettempdir())
