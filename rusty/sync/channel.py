"""Channel — multi-producer single-consumer message passing."""
from __future__ import annotations
"""Channel — multi-producer single-consumer channel.

Provides Channel, Sender, and Receiver for message passing between
threads. Supports bounded and unbounded channels.
"""

import queue as _queue
from typing import Any, Generic, Iterator, TypeVar

T = TypeVar("T")


class Sender(Generic[T]):
    __slots__ = ("_queue", "_closed")

    def __init__(self, queue: Any) -> None:
        self._queue = queue
        self._closed = False

    def send(self, value: T) -> bool:
        if self._closed:
            return False
        try:
            self._queue.put_nowait(value)
            return True
        except Exception:
            return False

    def is_closed(self) -> bool:
        return self._closed

    def close(self) -> None:
        self._closed = True

    def __enter__(self) -> Sender[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"Sender(closed={self._closed})"


class Receiver(Generic[T]):
    __slots__ = ("_queue", "_closed")

    def __init__(self, queue: Any) -> None:
        self._queue = queue
        self._closed = False

    def recv(self) -> T | None:
        try:
            return self._queue.get_nowait()
        except Exception:
            return None

    def recv_blocking(self, timeout: float | None = None) -> T | None:
        try:
            return self._queue.get(timeout=timeout)
        except Exception:
            return None

    def try_recv(self) -> T | None:
        return self.recv()

    def is_empty(self) -> bool:
        return self._queue.empty()

    def is_closed(self) -> bool:
        return self._closed

    def __enter__(self) -> Receiver[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self._closed = True

    def __iter__(self) -> Iterator[T]:
        while True:
            value = self.recv()
            if value is None:
                break
            yield value

    def __repr__(self) -> str:
        return f"Receiver(closed={self._closed})"


class Channel(Generic[T]):
    __slots__ = ("_sender", "_receiver")

    def __init__(self, capacity: int = 0) -> None:
        if capacity == 0:
            q: Any = _queue.SimpleQueue()
        else:
            q = _queue.Queue(maxsize=capacity)
        self._sender = Sender[T](q)
        self._receiver = Receiver[T](q)

    @classmethod
    def unbounded(cls) -> Channel[T]:
        return cls(0)

    @classmethod
    def bounded(cls, capacity: int) -> Channel[T]:
        return cls(capacity)

    @property
    def sender(self) -> Sender[T]:
        return self._sender

    @property
    def receiver(self) -> Receiver[T]:
        return self._receiver

    def send(self, value: T) -> bool:
        return self._sender.send(value)

    def recv(self) -> T | None:
        return self._receiver.recv()

    def __repr__(self) -> str:
        return f"Channel(sender={self._sender}, receiver={self._receiver})"
