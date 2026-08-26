"""BufReader and BufWriter — buffered I/O with configurable capacity."""
from __future__ import annotations

"""Buffered I/O — BufReader and BufWriter.

Provides BufReader for buffered reading and BufWriter for buffered
writing with configurable capacity and automatic flushing.
"""

from typing import Any

from .cursor import SeekFrom
from .read import BufSplitIter, LinesIter


class BufReader:
    __slots__ = ("_inner", "_buffer", "_pos", "_capacity")

    def __init__(self, inner: Any, capacity: int = 8192) -> None:
        self._inner = inner
        self._buffer = bytearray()
        self._pos = 0
        self._capacity = capacity

    @classmethod
    def with_capacity(cls, capacity: int, inner: Any) -> BufReader:  # type: ignore
        return cls(inner, capacity)

    def inner(self) -> Any:
        return self._inner

    def into_inner(self) -> Any:  # type: ignore
        return self._inner

    def buffer(self) -> bytes:  # type: ignore
        return bytes(self._buffer[self._pos:])

    def capacity(self) -> int:
        return self._capacity

    def set_capacity(self, capacity: int) -> None:  # type: ignore
        self._capacity = capacity

    def fill_buf(self) -> bytes:  # type: ignore
        if self._pos >= len(self._buffer):
            self._buffer = bytearray()
            self._pos = 0
            read_buf = bytearray(self._capacity)
            n = self._inner.read(read_buf)
            self._buffer = bytearray(read_buf[:n])
        return bytes(self._buffer[self._pos:])

    def consume(self, amt: int) -> None:  # type: ignore
        self._pos = min(self._pos + amt, len(self._buffer))

    def has_consumed(self) -> bool:
        return self._pos >= len(self._buffer)

    def read(self, buf: bytearray) -> int:  # type: ignore
        buffered = self.fill_buf()
        if not buffered:
            return self._inner.read(buf)  # type: ignore
        n = min(len(buf), len(buffered))
        buf[:n] = buffered[:n]
        self.consume(n)
        return n

    def read_exact(self, buf: bytearray) -> None:  # type: ignore
        total = 0
        needed = len(buf)
        while total < needed:
            n = self.read(buf[total:])
            if n == 0:
                raise IOError("failed to fill whole buffer")
            total += n

    def read_to_end(self) -> bytes:  # type: ignore
        chunks = [bytes(self._buffer[self._pos:])]
        self._buffer = bytearray()
        self._pos = 0
        while True:
            read_buf = bytearray(8192)
            n = self._inner.read(read_buf)
            if n == 0:
                break
            chunks.append(bytes(read_buf[:n]))
        return b"".join(chunks)

    def read_to_string(self) -> str:  # type: ignore
        return self.read_to_end().decode("utf-8")

    def read_until(self, byte: int) -> bytes:  # type: ignore
        buf = bytearray()
        while True:
            chunk = self.fill_buf()
            if not chunk:
                rest = self._inner.read_until(byte)  # type: ignore
                buf.extend(rest)
                return bytes(buf)
            idx = chunk.find(bytes([byte]))
            if idx >= 0:
                buf.extend(chunk[:idx + 1])
                self.consume(idx + 1)
                return bytes(buf)
            buf.extend(chunk)
            self.consume(len(chunk))

    def read_line(self) -> str:  # type: ignore
        return self.read_until(ord("\n")).decode("utf-8")

    def split(self, byte: int) -> BufSplitIter:  # type: ignore
        return BufSplitIter(self, byte)

    def lines(self) -> LinesIter:  # type: ignore
        return LinesIter(self)

    def seek(self, style: SeekFrom) -> int:  # type: ignore
        if hasattr(self._inner, 'seek'):
            self._buffer = bytearray()
            self._pos = 0
            return self._inner.seek(style)  # type: ignore
        raise IOError("underlying stream is not seekable")

    def __enter__(self) -> BufReader:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __repr__(self) -> str:
        return f"BufReader(buffered={len(self._buffer) - self._pos})"


class BufWriter:
    __slots__ = ("_inner", "_buffer", "_pos", "_closed", "_capacity")

    def __init__(self, inner: Any, capacity: int = 8192) -> None:
        self._inner = inner
        self._buffer = bytearray()
        self._pos = 0
        self._capacity = capacity
        self._closed = False

    @classmethod
    def with_capacity(cls, capacity: int, inner: Any) -> BufWriter:  # type: ignore
        return cls(inner, capacity)

    def inner(self) -> Any:
        return self._inner

    def into_inner(self) -> Any:  # type: ignore
        self.flush()
        return self._inner

    def buffer(self) -> bytes:  # type: ignore
        return bytes(self._buffer[self._pos:])

    def capacity(self) -> int:
        return self._capacity

    def write(self, data: bytes | bytearray | str) -> int:  # type: ignore
        if isinstance(data, str):
            data = data.encode("utf-8")
        if len(data) > self._capacity:
            self.flush()
            return self._inner.write(data)  # type: ignore
        if len(self._buffer) + len(data) > self._capacity:
            self.flush()
        self._buffer.extend(data)
        return len(data)

    def write_all(self, data: bytes | bytearray | str) -> None:  # type: ignore
        self.write(data)

    def flush(self) -> None:  # type: ignore
        if self._buffer:
            self._inner.write(bytes(self._buffer))  # type: ignore
            if hasattr(self._inner, 'flush'):
                self._inner.flush()
            self._buffer = bytearray()
            self._pos = 0

    def write_fmt(self, args: Any) -> None:  # type: ignore
        self.write(str(args))

    def seek(self, style: SeekFrom) -> int:  # type: ignore
        self.flush()
        if hasattr(self._inner, 'seek'):
            return self._inner.seek(style)  # type: ignore
        raise IOError("underlying stream is not seekable")

    def into_raw_fd(self) -> None:  # type: ignore
        self.flush()

    def __enter__(self) -> BufWriter:
        return self

    def __exit__(self, *_: Any) -> None:  # type: ignore
        self.flush()

    def __del__(self) -> None:
        try:
            self.flush()
        except Exception:
            pass

    def __repr__(self) -> str:
        return f"BufWriter(buffered={len(self._buffer)})"
