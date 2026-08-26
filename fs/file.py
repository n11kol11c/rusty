"""File and OpenOptions — file I/O with configurable open modes."""
from __future__ import annotations

"""File and OpenOptions — file I/O.

Provides File for reading/writing files and OpenOptions for
configurable file opening with read, write, append, create modes.
"""

import os
from typing import Any

from .path import Path
from .metadata import Metadata, Permissions, metadata_from_os


class OpenOptions:
    __slots__ = ("_read", "_write", "_append", "_truncate", "_create", "_create_new")

    def __init__(self) -> None:
        self._read = False
        self._write = False
        self._append = False
        self._truncate = False
        self._create = False
        self._create_new = False

    @classmethod
    def new(cls) -> OpenOptions:  # type: ignore
        return cls()

    def read(self, enable: bool = True) -> OpenOptions:
        self._read = enable
        return self

    def write(self, enable: bool = True) -> OpenOptions:
        self._write = enable
        return self

    def append(self, enable: bool = True) -> OpenOptions:
        self._append = enable
        return self

    def truncate(self, enable: bool = True) -> OpenOptions:
        self._truncate = enable
        return self

    def create(self, enable: bool = True) -> OpenOptions:
        self._create = enable
        return self

    def create_new(self, enable: bool = True) -> OpenOptions:
        self._create_new = enable
        return self

    def open(self, path: str | Path) -> File:
        path_str = path.as_str() if isinstance(path, Path) else str(path)

        if self._create_new and os.path.exists(path_str):
            raise FileExistsError(f"file already exists: {path_str}")

        mode = 'r'
        if self._create_new or (self._create and self._write):
            mode = 'w'
        elif self._write and self._append:
            mode = 'a'
        elif self._write:
            mode = 'w'
        elif self._read and self._write:
            mode = 'r+'
        elif self._read:
            mode = 'r'

        if self._truncate and mode in ('r+', 'w', 'a'):
            if mode == 'r+':
                mode = 'w'
            elif mode == 'a':
                mode = 'w'

        if 'w' in mode and not self._create and not os.path.exists(path_str):
            if not self._create:
                raise FileNotFoundError(f"no such file or directory: {path_str}")

        f = open(path_str, mode)  # type: ignore[arg-type]
        return File(f, path_str)

    def __repr__(self) -> str:  # type: ignore
        flags = []
        if self._read:
            flags.append("read")
        if self._write:
            flags.append("write")
        if self._append:
            flags.append("append")
        if self._truncate:
            flags.append("truncate")
        if self._create:
            flags.append("create")
        if self._create_new:
            flags.append("create_new")
        return f"OpenOptions({', '.join(flags)})"


class File:
    __slots__ = ("_handle", "_path", "_closed")

    def __init__(self, handle: Any, path: str = "") -> None:
        self._handle = handle
        self._path = path
        self._closed = False

    @classmethod
    def create(cls, path: str | Path) -> File:  # type: ignore
        path_str = path.as_str() if isinstance(path, Path) else str(path)
        return cls(open(path_str, 'w'), path_str)

    @classmethod
    def create_new(cls, path: str | Path) -> File:  # type: ignore
        path_str = path.as_str() if isinstance(path, Path) else str(path)
        if os.path.exists(path_str):
            raise FileExistsError(f"file already exists: {path_str}")
        return cls(open(path_str, 'w'), path_str)

    @classmethod
    def open(cls, path: str | Path) -> File:  # type: ignore
        path_str = path.as_str() if isinstance(path, Path) else str(path)
        return cls(open(path_str, 'r'), path_str)

    @classmethod
    def options(cls) -> OpenOptions:  # type: ignore
        return OpenOptions()

    def read(self) -> bytes:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.read()  # type: ignore

    def read_exact(self, buf: bytearray) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        data = self._handle.read(len(buf))  # type: ignore
        n = len(data)
        buf[:n] = data
        return n

    def read_to_string(self) -> str:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.read()  # type: ignore

    def write(self, data: bytes | str) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.write(data)  # type: ignore

    def write_all(self, data: bytes | str) -> None:  # type: ignore
        self.write(data)

    def flush(self) -> None:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        self._handle.flush()  # type: ignore

    def sync_all(self) -> None:  # type: ignore
        self.flush()

    def sync_data(self) -> None:  # type: ignore
        self.flush()

    def seek(self, pos: int) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.seek(pos)  # type: ignore

    def seek_from_start(self, offset: int) -> int:  # type: ignore
        return self.seek(offset)

    def seek_from_current(self, offset: int) -> int:  # type: ignore
        return self.seek(offset)

    def seek_from_end(self, offset: int) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.seek(offset, 2)  # type: ignore

    def stream_position(self) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.tell()  # type: ignore

    def set_len(self, size: int) -> None:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        self._handle.truncate(size)  # type: ignore

    def metadata(self) -> Metadata:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return metadata_from_os(self._path)

    def set_permissions(self, perm: Permissions) -> None:  # type: ignore
        os.chmod(self._path, 0o444 if perm.readonly() else 0o644)

    def path(self) -> Path:  # type: ignore
        return Path(self._path)

    def into_inner(self) -> Any:  # type: ignore
        self._closed = True
        return self._handle

    def try_clone(self) -> File:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        import io
        new_handle = open(self._path, self._handle.mode)  # type: ignore
        return File(new_handle, self._path)

    def __enter__(self) -> File:  # type: ignore
        return self

    def __exit__(self, *_: Any) -> None:  # type: ignore
        self.close()

    def close(self) -> None:  # type: ignore
        if not self._closed:
            self._handle.close()  # type: ignore
            self._closed = True

    def is_closed(self) -> bool:  # type: ignore
        return self._closed

    def __repr__(self) -> str:
        return f"File({self._path!r}, closed={self._closed})"
