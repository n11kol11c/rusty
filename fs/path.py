"""Path and PathBuf — filesystem path manipulation."""
from __future__ import annotations

"""Path and PathBuf — filesystem path types.

Provides Path for immutable paths and PathBuf for mutable paths
with join, parent, extension, file_name, and filesystem operations.
"""

import os

from .metadata import Metadata, DirEntry, ReadDir, metadata_from_os


class Path:
    __slots__ = ("_path",)

    def __init__(self, path: str | os.PathLike) -> None:
        self._path = os.fspath(path) if isinstance(path, os.PathLike) else path

    @classmethod
    def new(cls, path: str) -> Path:  # type: ignore
        return cls(path)

    def as_str(self) -> str:
        return self._path

    def to_str(self) -> str | None:
        return self._path

    def to_string_lossy(self) -> str:
        return self._path

    def to_path_buf(self) -> PathBuf:  # type: ignore
        return PathBuf(self._path)

    def as_os_str(self) -> str:  # type: ignore
        return self._path

    def is_absolute(self) -> bool:
        return os.path.isabs(self._path)

    def is_relative(self) -> bool:  # type: ignore
        return not self.is_absolute()

    def is_relative_to(self, base: str | Path) -> bool:  # type: ignore
        base_str = base.as_str() if isinstance(base, Path) else str(base)
        try:
            os.path.relpath(self._path, base_str)
            return True
        except ValueError:
            return False

    def starts_with(self, base: str | Path) -> bool:  # type: ignore
        base_str = base.as_str() if isinstance(base, Path) else str(base)
        return os.path.commonpath([self._path, base_str]) == base_str or self._path == base_str

    def ends_with(self, ext: str | Path) -> bool:  # type: ignore
        ext_str = ext.as_str() if isinstance(ext, Path) else str(ext)
        return self._path.endswith(ext_str)

    def parent(self) -> Path | None:
        parent = os.path.dirname(self._path)
        if not parent:
            return None
        return Path(parent)

    def file_name(self) -> str | None:  # type: ignore
        return os.path.basename(self._path) or None

    def extension(self) -> str | None:  # type: ignore
        _, ext = os.path.splitext(self._path)
        return ext[1:] if ext else None

    def file_stem(self) -> str | None:  # type: ignore
        stem, _ = os.path.splitext(os.path.basename(self._path))
        return stem or None

    def with_extension(self, ext: str) -> Path:  # type: ignore
        base, _ = os.path.splitext(self._path)
        if ext and not ext.startswith('.'):
            ext = '.' + ext
        return Path(base + ext)

    def join(self, other: str | Path) -> Path:
        other_str = other.as_str() if isinstance(other, Path) else other
        return Path(os.path.join(self._path, other_str))

    def __truediv__(self, other: str | Path) -> Path:
        return self.join(other)

    def __rtruediv__(self, other: str | Path) -> Path:
        other_str = other.as_str() if isinstance(other, Path) else other
        return Path(os.path.join(other_str, self._path))

    def exists(self) -> bool:
        return os.path.exists(self._path)

    def is_file(self) -> bool:  # type: ignore
        return os.path.isfile(self._path)

    def is_dir(self) -> bool:  # type: ignore
        return os.path.isdir(self._path)

    def is_symlink(self) -> bool:  # type: ignore
        return os.path.islink(self._path)

    def metadata(self) -> Metadata:  # type: ignore
        return metadata_from_os(self._path)

    def canonicalize(self) -> Path:  # type: ignore
        return Path(os.path.realpath(self._path))

    def normalize(self) -> Path:  # type: ignore
        return Path(os.path.normpath(self._path))

    def display(self) -> str:
        return self._path

    def to_absolute(self) -> Path:  # type: ignore
        return Path(os.path.abspath(self._path))

    def read_to_string(self) -> str:  # type: ignore
        with open(self._path, 'r') as f:
            return f.read()

    def read_to_bytes(self) -> bytes:  # type: ignore
        with open(self._path, 'rb') as f:
            return f.read()

    def write_str(self, data: str) -> None:  # type: ignore
        with open(self._path, 'w') as f:
            f.write(data)

    def write_bytes(self, data: bytes) -> None:  # type: ignore
        with open(self._path, 'wb') as f:
            f.write(data)

    def create_dir(self) -> None:  # type: ignore
        os.makedirs(self._path, exist_ok=True)

    def create_dir_all(self) -> None:  # type: ignore
        os.makedirs(self._path, exist_ok=True)

    def remove_file(self) -> None:  # type: ignore
        os.remove(self._path)

    def remove_dir(self) -> None:  # type: ignore
        os.rmdir(self._path)

    def remove_dir_all(self) -> None:  # type: ignore
        import shutil
        shutil.rmtree(self._path)

    def rename(self, to: str | Path) -> None:  # type: ignore
        to_str = to.as_str() if isinstance(to, Path) else str(to)
        os.rename(self._path, to_str)

    def copy(self, to: str | Path) -> None:  # type: ignore
        import shutil
        to_str = to.as_str() if isinstance(to, Path) else str(to)
        shutil.copy2(self._path, to_str)

    def read_dir(self) -> ReadDir:
        return ReadDir(self._path)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Path):
            return os.path.normpath(self._path) == os.path.normpath(other._path)
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Path):
            return os.path.normpath(self._path) != os.path.normpath(other._path)
        return NotImplemented

    def __lt__(self, other: Path) -> bool:
        if isinstance(other, Path):
            return os.path.normpath(self._path) < os.path.normpath(other._path)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(os.path.normpath(self._path))

    def __fspath__(self) -> str:
        return self._path

    def __str__(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return f"Path({self._path!r})"


class PathBuf:
    __slots__ = ("_path",)

    def __init__(self, path: str | os.PathLike | Path = "") -> None:
        if isinstance(path, Path):
            self._path = path.as_str()
        else:
            self._path = os.fspath(path) if isinstance(path, os.PathLike) else path

    @classmethod
    def new(cls) -> PathBuf:  # type: ignore
        return cls("")

    @classmethod
    def from_str(cls, s: str) -> PathBuf:  # type: ignore
        return cls(s)

    def as_path(self) -> Path:
        return Path(self._path)

    def as_str(self) -> str:
        return self._path

    def into_string(self) -> str:  # type: ignore
        return self._path

    def push(self, path: str | Path) -> None:  # type: ignore
        if isinstance(path, Path):
            self._path = os.path.join(self._path, path.as_str())
        else:
            self._path = os.path.join(self._path, path)

    def push_str(self, s: str) -> None:  # type: ignore
        self._path = os.path.join(self._path, s)

    def pop(self) -> bool:  # type: ignore
        parent = os.path.dirname(self._path)
        if parent == self._path:
            return False
        self._path = parent
        return True

    def set_extension(self, ext: str) -> bool:  # type: ignore
        base, _ = os.path.splitext(self._path)
        if ext and not ext.startswith('.'):
            ext = '.' + ext
        self._path = base + ext
        return True

    def clear(self) -> None:  # type: ignore
        self._path = ""

    def into_boxed(self) -> Path:  # type: ignore
        return Path(self._path)

    def is_absolute(self) -> bool:  # type: ignore
        return os.path.isabs(self._path)

    def parent(self) -> Path | None:  # type: ignore
        parent = os.path.dirname(self._path)
        if not parent:
            return None
        return Path(parent)

    def file_name(self) -> str | None:  # type: ignore
        return os.path.basename(self._path) or None

    def extension(self) -> str | None:  # type: ignore
        _, ext = os.path.splitext(self._path)
        return ext[1:] if ext else None

    def join(self, other: str | Path) -> PathBuf:  # type: ignore
        other_str = other.as_str() if isinstance(other, Path) else other
        return PathBuf(os.path.join(self._path, other_str))

    def canonicalize(self) -> PathBuf:  # type: ignore
        return PathBuf(os.path.realpath(self._path))

    def normalize(self) -> PathBuf:  # type: ignore
        return PathBuf(os.path.normpath(self._path))

    def exists(self) -> bool:  # type: ignore
        return os.path.exists(self._path)

    def __truediv__(self, other: str | Path) -> PathBuf:  # type: ignore
        return self.join(other)

    def __str__(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return f"PathBuf({self._path!r})"
