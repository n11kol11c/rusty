"""Command — build and spawn child processes."""
from __future__ import annotations

"""Command — process spawning builder.

Provides Command for configuring and spawning child processes
with arg, env, current_dir, stdin/stdout/stderr, spawn, output.
"""

import subprocess
from typing import Any, Iterable

from .child import Child, Stdio
from .output import ExitStatus, Output
from ..fs.path import Path


class Command:
    __slots__ = ("_program", "_args", "_env", "_cwd", "_stdin", "_stdout", "_stderr")

    def __init__(self, program: str | Path) -> None:
        program_str = program.as_str() if isinstance(program, Path) else str(program)
        self._program = program_str
        self._args: list[str] = []
        self._env: dict[str, str] | None = None
        self._cwd: str | None = None
        self._stdin: Stdio = Stdio.inherit()
        self._stdout: Stdio = Stdio.inherit()
        self._stderr: Stdio = Stdio.inherit()

    def arg(self, arg: str) -> Command:  # type: ignore
        self._args.append(str(arg))
        return self

    def args(self, args: Iterable[str]) -> Command:  # type: ignore
        for a in args:
            self._args.append(str(a))
        return self

    def env(self, key: str, val: str) -> Command:  # type: ignore
        if self._env is None:
            self._env = {}
        self._env[key] = val
        return self

    def envs(self, envs: dict[str, str]) -> Command:  # type: ignore
        if self._env is None:
            self._env = {}
        self._env.update(envs)
        return self

    def current_dir(self, dir: str | Path) -> Command:  # type: ignore
        self._cwd = dir.as_str() if isinstance(dir, Path) else str(dir)
        return self

    def stdin(self, cfg: Stdio) -> Command:  # type: ignore
        self._stdin = cfg
        return self

    def stdout(self, cfg: Stdio) -> Command:  # type: ignore
        self._stdout = cfg
        return self

    def stderr(self, cfg: Stdio) -> Command:  # type: ignore
        self._stderr = cfg
        return self

    def spawn(self) -> Child:  # type: ignore
        stdin_cfg = None
        stdout_cfg = None
        stderr_cfg = None

        if self._stdin._kind == Stdio.PIPED:
            stdin_cfg = subprocess.PIPE
        elif self._stdin._kind == Stdio.NULL:
            stdin_cfg = subprocess.DEVNULL

        if self._stdout._kind == Stdio.PIPED:
            stdout_cfg = subprocess.PIPE
        elif self._stdout._kind == Stdio.NULL:
            stdout_cfg = subprocess.DEVNULL

        if self._stderr._kind == Stdio.PIPED:
            stderr_cfg = subprocess.PIPE
        elif self._stderr._kind == Stdio.NULL:
            stderr_cfg = subprocess.DEVNULL

        proc = subprocess.Popen(
            [self._program] + self._args,
            stdin=stdin_cfg,
            stdout=stdout_cfg,
            stderr=stderr_cfg,
            env=self._env,
            cwd=self._cwd,
        )
        return Child(proc)

    def output(self) -> Output:  # type: ignore
        env = self._env
        proc = subprocess.run(
            [self._program] + self._args,
            capture_output=True,
            env=env,
            cwd=self._cwd,
        )
        return Output(
            ExitStatus(proc.returncode),
            proc.stdout,
            proc.stderr,
        )

    def status(self) -> ExitStatus:  # type: ignore
        proc = subprocess.run(
            [self._program] + self._args,
            capture_output=False,
            env=self._env,
            cwd=self._cwd,
        )
        return ExitStatus(proc.returncode)

    def get_program(self) -> str:  # type: ignore
        return self._program

    def get_args(self) -> list[str]:  # type: ignore
        return self._args.copy()

    def __repr__(self) -> str:
        return f"Command({self._program!r})"
