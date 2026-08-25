"""Read and BufRead traits — byte reading and buffered reading."""
from __future__ import annotations

"""Read and BufRead traits — reading abstraction.

Provides Read for byte reading and BufRead for buffered reading
with fill_buf, consume, read_until, read_line, split, and lines.
"""

from typing import Any


class Read:
    def read(self, buf: bytearray) -> int:  # type: ignore
        raise NotImplementedError

    def read_exact(self, buf: bytearray) -> None:  # type: ignore
        total = 0
        needed = len(buf)
        while total < needed:
            n = self.read(buf[total:])
            if n == 0:
                raise IOError("failed to fill whole buffer")
            total += n

    def read_to_end(self) -> bytes:  # type: ignore
        chunks = []
        while True:
            chunk = self.read(8192)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)

    def read_to_string(self) -> str:  # type: ignore
        return self.read_to_end().decode("utf-8")

    def by_ref(self) -> Any:  # type: ignore
        return self


class BufRead:
    def fill_buf(self) -> bytes:  # type: ignore
        raise NotImplementedError

    def consume(self, amt: int) -> None:  # type: ignore
        pass

    def has_consumed(self) -> bool:  # type: ignore
        return False

    def read_until(self, byte: int) -> bytes:  # type: ignore
        buf = bytearray()
        while True:
            chunk = self.fill_buf()
            if not chunk:
                break
            idx = chunk.find(bytes([byte]))
            if idx >= 0:
                buf.extend(chunk[:idx + 1])
                self.consume(idx + 1)
                return bytes(buf)
            buf.extend(chunk)
            self.consume(len(chunk))
        return bytes(buf)

    def read_line(self) -> str:  # type: ignore
        return self.read_until(ord("\n")).decode("utf-8")

    def split(self, byte: int) -> BufSplitIter:  # type: ignore
        return BufSplitIter(self, byte)

    def lines(self) -> LinesIter:  # type: ignore
        return LinesIter(self)


class BufSplitIter:
    __slots__ = ("_reader", "_byte", "_done")

    def __init__(self, reader: BufRead, byte: int) -> None:
        self._reader = reader
        self._byte = byte
        self._done = False

    def __iter__(self) -> BufSplitIter:
        return self

    def __next__(self) -> bytes:
        if self._done:
            raise StopIteration
        result = self._reader.read_until(self._byte)
        if not result:
            self._done = True
            raise StopIteration
        return result


class LinesIter:
    __slots__ = ("_reader", "_done")

    def __init__(self, reader: BufRead) -> None:
        self._reader = reader
        self._done = False

    def __iter__(self) -> LinesIter:
        return self

    def __next__(self) -> str:
        if self._done:
            raise StopIteration
        line = self._reader.read_line()
        if not line:
            self._done = True
            raise StopIteration
        return line
