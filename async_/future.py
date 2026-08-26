"""Future, Poll, Waker, Stream, JoinHandle — async computation and task management."""
from __future__ import annotations

"""Future, Poll, Waker, Stream — async computation primitives.

Provides Future[T] for async computations, Poll[T] for pending/ready
state, Waker for task notification, Stream[T] for async iteration,
JoinHandle for task results, and spawn for launching tasks.
"""

import asyncio
import threading
from typing import Any, Callable, Generic, Iterable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class Poll(Generic[T]):
    __slots__ = ("_ready", "_value")

    def __init__(self, ready: bool, value: T | None = None) -> None:
        self._ready = ready
        self._value = value

    @classmethod
    def ready(cls, value: T) -> Poll[T]:
        return cls(True, value)

    @classmethod
    def pending(cls) -> Poll[T]:
        return cls(False)

    def is_ready(self) -> bool:
        return self._ready

    def is_pending(self) -> bool:
        return not self._ready

    def unwrap(self) -> T:
        if not self._ready:
            raise RuntimeError("called unwrap on pending Poll")
        return self._value  # type: ignore

    def unwrap_or(self, default: T) -> T:
        if not self._ready:
            return default
        return self._value  # type: ignore

    def map(self, fn: Callable[[T], U]) -> Poll[U]:
        if self._ready:
            return Poll.ready(fn(self._value))  # type: ignore
        return Poll.pending()

    def and_then(self, fn: Callable[[T], Poll[U]]) -> Poll[U]:
        if self._ready:
            return fn(self._value)  # type: ignore
        return Poll.pending()

    def inspect(self, fn: Callable[[T], Any]) -> Poll[T]:
        if self._ready:
            fn(self._value)  # type: ignore
        return self

    def __repr__(self) -> str:
        if self._ready:
            return f"Poll::Ready({self._value!r})"
        return "Poll::Pending"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Poll):
            if self._ready != other._ready:
                return False
            if self._ready:
                return self._value == other._value
            return True
        return NotImplemented

    def __bool__(self) -> bool:
        return self._ready


class Waker:
    __slots__ = ("_wake_fn", "_woken")

    def __init__(self, wake_fn: Callable[[], None] | None = None) -> None:
        self._wake_fn = wake_fn
        self._woken = False

    def wake(self) -> None:
        self._woken = True
        if self._wake_fn:
            self._wake_fn()

    def wake_by_ref(self) -> None:
        self.wake()

    def clone_waker(self) -> Waker:
        return Waker(self._wake_fn)

    def is_woken(self) -> bool:
        return self._woken

    def reset(self) -> None:
        self._woken = False

    def __repr__(self) -> str:
        return f"Waker(woken={self._woken})"


class JoinHandle(Generic[T]):
    __slots__ = ("_future", "_result", "_done", "_exception", "_thread")

    def __init__(self, future: Future[T]) -> None:
        self._future = future
        self._result: T | None = None
        self._done = False
        self._exception: Exception | None = None
        self._thread: threading.Thread | None = None

    def run(self) -> None:
        try:
            loop = asyncio.new_event_loop()
            self._result = loop.run_until_complete(self._future)
            loop.close()
        except Exception as e:
            self._exception = e
        finally:
            self._done = True

    def start(self) -> None:
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def is_finished(self) -> bool:
        return self._done

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def abort(self) -> bool:
        if self._thread and self._thread.is_alive():
            return False
        return True

    def get_result(self, timeout: float | None = None) -> T | None:
        if self._thread:
            self._thread.join(timeout=timeout)
        if self._exception:
            raise self._exception
        return self._result

    def join(self, timeout: float | None = None) -> T | None:
        return self.get_result(timeout)

    def __enter__(self) -> JoinHandle[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        if self._thread:
            self._thread.join()

    def __repr__(self) -> str:
        return f"JoinHandle(finished={self._done})"


class Stream(Generic[T]):
    __slots__ = ("_async_gen", "_buffer")

    def __init__(self, async_gen: Any = None) -> None:
        self._async_gen = async_gen
        self._buffer: list[T] = []

    @classmethod
    def from_iter(cls, iterable: Iterable[T]) -> Stream[T]:
        async def gen():
            for v in iterable:
                yield v
        return cls(gen())

    @classmethod
    def from_async_iter(cls, async_iter: Any) -> Stream[T]:
        return cls(async_iter)

    @classmethod
    def empty(cls) -> Stream[T]:
        async def gen():
            return
            yield  # type: ignore[misc]
        return cls(gen())

    @classmethod
    def once(cls, value: T) -> Stream[T]:
        async def gen():
            yield value
        return cls(gen())

    @classmethod
    def repeat(cls, value: T) -> Stream[T]:
        async def gen():
            while True:
                yield value
        return cls(gen())

    @classmethod
    def chain(cls, *streams: Stream[T]) -> Stream[T]:
        async def gen():
            for s in streams:
                async for item in s._async_gen:
                    yield item
        return cls(gen())

    async def next(self) -> T | None:
        try:
            return await self._async_gen.__anext__()
        except StopAsyncIteration:
            return None

    async def map(self, fn: Callable[[T], U]) -> Stream[U]:
        async def gen():
            async for item in self._async_gen:
                yield fn(item)
        return Stream(gen())

    async def filter(self, predicate: Callable[[T], bool]) -> Stream[T]:
        async def gen():
            async for item in self._async_gen:
                if predicate(item):
                    yield item
        return Stream(gen())

    async def take(self, n: int) -> Stream[T]:
        async def gen():
            count = 0
            async for item in self._async_gen:
                if count >= n:
                    break
                yield item
                count += 1
        return Stream(gen())

    async def collect(self) -> list[T]:
        result = []
        async for item in self._async_gen:
            result.append(item)
        return result

    async def fold(self, init: U, fn: Callable[[U, T], U]) -> U:
        acc = init
        async for item in self._async_gen:
            acc = fn(acc, item)
        return acc

    async def for_each(self, fn: Callable[[T], Any]) -> None:
        async for item in self._async_gen:
            fn(item)

    async def count(self) -> int:
        n = 0
        async for _ in self._async_gen:
            n += 1
        return n

    async def first(self) -> T | None:
        return await self.next()

    async def peek(self) -> T | None:
        try:
            item = await self._async_gen.__anext__()
            self._buffer.append(item)
            return item
        except StopAsyncIteration:
            return None

    def __aiter__(self) -> Any:
        return self._async_gen

    def __repr__(self) -> str:
        return "Stream(...)"


class Future(Generic[T]):
    __slots__ = ("_coro", "_done", "_result", "_exception", "_callbacks")

    def __init__(self, coro: Any = None) -> None:
        self._coro = coro
        self._done = False
        self._result: T | None = None
        self._exception: Exception | None = None
        self._callbacks: list[Callable[[Future[T]], None]] = []

    @classmethod
    def ready(cls, value: T) -> Future[T]:
        f = cls()
        f._done = True
        f._result = value
        return f

    @classmethod
    def pending(cls) -> Future[T]:
        return cls()

    def poll(self, waker: Waker | None = None) -> Poll[T]:
        if self._done:
            if self._exception:
                raise self._exception
            return Poll.ready(self._result)  # type: ignore
        return Poll.pending()

    def is_done(self) -> bool:
        return self._done

    def result(self) -> T | None:
        return self._result

    def exception(self) -> Exception | None:
        return self._exception

    def add_done_callback(self, fn: Callable[[Future[T]], None]) -> None:
        if self._done:
            fn(self)
        else:
            self._callbacks.append(fn)

    def set_result(self, value: T) -> None:
        self._result = value
        self._done = True
        for cb in self._callbacks:
            cb(self)

    def set_exception(self, exc: Exception) -> None:
        self._exception = exc
        self._done = True
        for cb in self._callbacks:
            cb(self)

    def map(self, fn: Callable[[T], U]) -> Future[U]:
        async def mapped():
            result = await self
            return fn(result)
        return Future(mapped())

    def and_then(self, fn: Callable[[T], Future[U]]) -> Future[U]:
        async def chained():
            result = await self
            return await fn(result)
        return Future(chained())

    def __await__(self) -> Any:
        if self._coro is not None:
            return self._coro.__await__()
        if self._done:
            if self._exception:
                raise self._exception
            async def _ready():
                return self._result
            return _ready().__await__()
        async def _pending():
            return None
        return _pending().__await__()

    def __repr__(self) -> str:
        if self._done:
            return f"Future::Ready({self._result!r})"
        return "Future::Pending"


def spawn(coro: Any) -> JoinHandle:
    future = Future(coro)
    handle = JoinHandle(future)
    handle.start()
    return handle


async def join_all(handles: list[JoinHandle]) -> list:
    results = []
    for h in handles:
        results.append(h.get_result())
    return results
