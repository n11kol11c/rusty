"""Miscellaneous types — Ordering, ControlFlow, Reverse, Wrapping, Saturating, NonZero, SmallVec, ArrayVec, TinyVec, BitVec."""
from __future__ import annotations

"""Miscellaneous types — ordering, arithmetic, and small-vector optimization.

Provides Ordering, ControlFlow, Reverse, Wrapping, Saturating, NonZero,
SmallVec, ArrayVec, TinyVec, BitVec, and CreateMeta.
"""

from dataclasses import dataclass
from typing import Any, Callable, Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


class Ordering:
    __slots__ = ("_kind",)

    LESS = -1
    EQUAL = 0
    GREATER = 1

    def __init__(self, kind: int) -> None:
        self._kind = kind

    @classmethod
    def less(cls) -> Ordering:
        return cls(cls.LESS)

    @classmethod
    def equal(cls) -> Ordering:
        return cls(cls.EQUAL)

    @classmethod
    def greater(cls) -> Ordering:
        return cls(cls.GREATER)

    @classmethod
    def from_cmp(cls, a: Any, b: Any) -> Ordering:  # type: ignore
        if a < b:
            return cls(cls.LESS)
        if a > b:
            return cls(cls.GREATER)
        return cls(cls.EQUAL)

    def reverse(self) -> Ordering:
        return Ordering(-self._kind)

    def then(self, other: Ordering) -> Ordering:  # type: ignore
        if self._kind != 0:
            return self
        return other

    def then_with(self, f: Callable[[], Ordering]) -> Ordering:  # type: ignore
        if self._kind != 0:
            return self
        return f()

    def is_less(self) -> bool:  # type: ignore
        return self._kind < 0

    def is_equal(self) -> bool:  # type: ignore
        return self._kind == 0

    def is_greater(self) -> bool:  # type: ignore
        return self._kind > 0

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ordering):
            return self._kind == other._kind
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Ordering):
            return self._kind != other._kind
        return NotImplemented

    def __lt__(self, other: Ordering) -> bool:
        if isinstance(other, Ordering):
            return self._kind < other._kind
        return NotImplemented

    def __le__(self, other: Ordering) -> bool:
        if isinstance(other, Ordering):
            return self._kind <= other._kind
        return NotImplemented

    def __gt__(self, other: Ordering) -> bool:
        if isinstance(other, Ordering):
            return self._kind > other._kind
        return NotImplemented

    def __ge__(self, other: Ordering) -> bool:
        if isinstance(other, Ordering):
            return self._kind >= other._kind
        return NotImplemented

    def __hash__(self) -> int:
        return self._kind

    def __repr__(self) -> str:
        if self._kind < 0:
            return "Ordering::Less"
        if self._kind == 0:
            return "Ordering::Equal"
        return "Ordering::Greater"


class ControlFlow:
    __slots__ = ("_break", "_value", "_is_break")

    def __init__(self, is_break: bool = False, value: Any = None) -> None:
        self._is_break = is_break
        self._value = value

    @classmethod
    def cont(cls, value: Any = None) -> ControlFlow:
        return cls(False, value)

    @classmethod
    def brk(cls, value: Any = None) -> ControlFlow:
        return cls(True, value)

    def is_break(self) -> bool:  # type: ignore
        return self._is_break

    def is_continue(self) -> bool:  # type: ignore
        return not self._is_break

    def break_value(self) -> Any | None:  # type: ignore
        if self._is_break:
            return self._value
        return None

    def continue_value(self) -> Any | None:  # type: ignore
        if not self._is_break:
            return self._value
        return None

    def map_break(self, f: Callable[[Any], Any]) -> ControlFlow:  # type: ignore
        if self._is_break:
            return ControlFlow(True, f(self._value))
        return self

    def map_continue(self, f: Callable[[Any], Any]) -> ControlFlow:  # type: ignore
        if not self._is_break:
            return ControlFlow(False, f(self._value))
        return self

    def __repr__(self) -> str:
        if self._is_break:
            return f"ControlFlow::Break({self._value!r})"
        return f"ControlFlow::Continue({self._value!r})"


class Reverse(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def into_inner(self) -> T:  # type: ignore
        return self._value

    def as_ref(self) -> Any:  # type: ignore
        return self._value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Reverse):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Reverse):
            return self._value != other._value
        return NotImplemented

    def __lt__(self, other: Reverse) -> bool:
        if isinstance(other, Reverse):
            return other._value < self._value
        return NotImplemented

    def __le__(self, other: Reverse) -> bool:
        if isinstance(other, Reverse):
            return other._value <= self._value
        return NotImplemented

    def __gt__(self, other: Reverse) -> bool:
        if isinstance(other, Reverse):
            return other._value > self._value
        return NotImplemented

    def __ge__(self, other: Reverse) -> bool:
        if isinstance(other, Reverse):
            return other._value >= self._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"Reverse({self._value!r})"


class Wrapping(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def new(val: T) -> Wrapping[T]:
        return Wrapping(val)

    def into_inner(self) -> T:
        return self._value

    def wrapping_add(self, other: T) -> Wrapping[T]:
        return Wrapping((int(self._value) + int(other)) & 0xFFFFFFFF)

    def wrapping_sub(self, other: T) -> Wrapping[T]:
        return Wrapping((int(self._value) - int(other)) & 0xFFFFFFFF)

    def wrapping_mul(self, other: T) -> Wrapping[T]:
        return Wrapping((int(self._value) * int(other)) & 0xFFFFFFFF)

    def wrapping_div(self, other: T) -> Wrapping[T]:  # type: ignore
        if int(other) == 0:
            return Wrapping(0)
        return Wrapping((int(self._value) // int(other)) & 0xFFFFFFFF)

    def wrapping_neg(self) -> Wrapping[int]:  # type: ignore
        return Wrapping((-int(self._value)) & 0xFFFFFFFF)

    def __add__(self, other: Wrapping | int) -> Wrapping:
        if isinstance(other, Wrapping):
            return self.wrapping_add(other._value)
        return self.wrapping_add(other)

    def __sub__(self, other: Wrapping | int) -> Wrapping:
        if isinstance(other, Wrapping):
            return self.wrapping_sub(other._value)
        return self.wrapping_sub(other)

    def __mul__(self, other: Wrapping | int) -> Wrapping:
        if isinstance(other, Wrapping):
            return self.wrapping_mul(other._value)
        return self.wrapping_mul(other)

    def __floordiv__(self, other: Wrapping | int) -> Wrapping:
        if isinstance(other, Wrapping):
            return self.wrapping_div(other._value)
        return self.wrapping_div(other)

    def __neg__(self) -> Wrapping:
        return self.wrapping_neg()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Wrapping):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"Wrapping({self._value})"


class Saturating(Generic[T]):
    __slots__ = ("_value",)

    MAX = 2**31 - 1
    MIN = -(2**31)

    def __init__(self, value: T) -> None:
        self._value = value

    def new(val: T) -> Saturating[T]:
        return Saturating(val)

    def into_inner(self) -> T:
        return self._value

    def saturating_add(self, other: T) -> Saturating[T]:
        result = int(self._value) + int(other)
        return Saturating(max(self.MIN, min(self.MAX, result)))

    def saturating_sub(self, other: T) -> Saturating[T]:
        result = int(self._value) - int(other)
        return Saturating(max(self.MIN, min(self.MAX, result)))

    def saturating_mul(self, other: T) -> Saturating[T]:
        result = int(self._value) * int(other)
        return Saturating(max(self.MIN, min(self.MAX, result)))

    def __add__(self, other: Saturating | int) -> Saturating:
        if isinstance(other, Saturating):
            return self.saturating_add(other._value)
        return self.saturating_add(other)

    def __sub__(self, other: Saturating | int) -> Saturating:
        if isinstance(other, Saturating):
            return self.saturating_sub(other._value)
        return self.saturating_sub(other)

    def __mul__(self, other: Saturating | int) -> Saturating:
        if isinstance(other, Saturating):
            return self.saturating_mul(other._value)
        return self.saturating_mul(other)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Saturating):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"Saturating({self._value})"


class NonZero(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        if value == 0:
            raise ValueError("NonZero cannot be zero")
        self._value = value

    @classmethod
    def new(cls, value: T) -> NonZero[T]:  # type: ignore
        return cls(value)

    @classmethod
    def try_new(cls, value: T) -> NonZero[T] | None:  # type: ignore
        if value == 0:
            return None
        return cls(value)

    @classmethod
    def from_unsigned(cls, value: int) -> NonZero[int]:  # type: ignore
        if value <= 0:
            raise ValueError("value must be positive")
        return cls(value)

    def get(self) -> T:
        return self._value

    def checked_add(self, other: int) -> NonZero[T] | None:  # type: ignore
        result = int(self._value) + other
        if result == 0:
            return None
        return NonZero(result)

    def checked_sub(self, other: int) -> NonZero[T] | None:  # type: ignore
        result = int(self._value) - other
        if result == 0:
            return None
        return NonZero(result)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NonZero):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, NonZero):
            return self._value != other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"NonZero({self._value})"


class SmallVec(Generic[T]):
    __slots__ = ("_data", "_inline", "_stack_limit")

    def __init__(self, items: Iterable[T] | None = None, stack_limit: int = 8) -> None:
        self._stack_limit = stack_limit
        self._inline: list[T] = []
        self._data: list[T] = []
        if items:
            for item in items:
                self.push(item)

    @classmethod
    def from_vec(cls, vec: list[T]) -> SmallVec[T]:
        v = cls(stack_limit=8)
        for item in vec:
            v.push(item)
        return v

    def push(self, item: T) -> None:
        if len(self._inline) < self._stack_limit:
            self._inline.append(item)
        else:
            self._data.append(item)

    def pop(self) -> T | None:  # type: ignore
        if self._data:
            return self._data.pop()
        if self._inline:
            return self._inline.pop()
        return None

    def len(self) -> int:  # type: ignore
        return len(self._inline) + len(self._data)

    def is_empty(self) -> bool:  # type: ignore
        return self.len() == 0

    def capacity(self) -> int:  # type: ignore
        return self._stack_limit + len(self._data)

    def clear(self) -> None:  # type: ignore
        self._inline.clear()
        self._data.clear()

    def swap_remove(self, index: int) -> T:  # type: ignore
        if index < len(self._inline):
            last_idx = len(self._inline) - 1
            self._inline[index], self._inline[last_idx] = self._inline[last_idx], self._inline[index]
            return self._inline.pop()
        offset = len(self._inline)
        local_idx = index - offset
        last_idx = len(self._data) - 1
        self._data[local_idx], self._data[last_idx] = self._data[last_idx], self._data[local_idx]
        return self._data.pop()

    def retain(self, f: Callable[[T], bool]) -> None:  # type: ignore
        self._inline = [x for x in self._inline if f(x)]
        self._data = [x for x in self._data if f(x)]

    def drain(self) -> Drain[T]:  # type: ignore
        items = self._inline + self._data
        self._inline.clear()
        self._data.clear()
        return Drain(items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._inline + self._data)

    def __getitem__(self, index: int) -> T:
        if index < len(self._inline):
            return self._inline[index]
        return self._data[index - len(self._inline)]

    def __setitem__(self, index: int, value: T) -> None:
        if index < len(self._inline):
            self._inline[index] = value
        else:
            self._data[index - len(self._inline)] = value

    def __len__(self) -> int:
        return self.len()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        return f"SmallVec({list(self)})"


class ArrayVec(Generic[T]):
    __slots__ = ("_data", "_capacity", "_len")

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._data: list[T] = []
        self._len = 0

    @classmethod
    def with_capacity(cls, capacity: int) -> ArrayVec[T]:  # type: ignore
        return cls(capacity)

    def push(self, item: T) -> None:
        if self._len >= self._capacity:
            raise OverflowError("ArrayVec is full")
        self._data.append(item)
        self._len += 1

    def pop(self) -> T | None:  # type: ignore
        if self._len > 0:
            self._len -= 1
            return self._data.pop()
        return None

    def len(self) -> int:  # type: ignore
        return self._len

    def capacity(self) -> int:  # type: ignore
        return self._capacity

    def is_empty(self) -> bool:  # type: ignore
        return self._len == 0

    def is_full(self) -> bool:  # type: ignore
        return self._len >= self._capacity

    def clear(self) -> None:  # type: ignore
        self._data.clear()
        self._len = 0

    def truncate(self, len: int) -> None:  # type: ignore
        if len < self._len:
            self._data = self._data[:len]
            self._len = len

    def as_slice(self) -> list[T]:  # type: ignore
        return self._data[:self._len]

    def __iter__(self) -> Iterator[T]:
        return iter(self._data[:self._len])

    def __getitem__(self, index: int) -> T:
        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        self._data[index] = value

    def __len__(self) -> int:
        return self._len

    def __bool__(self) -> bool:
        return self._len > 0

    def __repr__(self) -> str:
        return f"ArrayVec({self._data[:self._len]})"


class TinyVec(Generic[T]):
    __slots__ = ("_inline", "_heap", "_is_inline")

    INLINE_LIMIT = 8

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._inline: list[T] = []
        self._heap: list[T] = []
        self._is_inline = True
        if items:
            for item in items:
                self.push(item)

    def push(self, item: T) -> None:
        if self._is_inline and len(self._inline) < self.INLINE_LIMIT:
            self._inline.append(item)
        else:
            if self._is_inline:
                self._heap = self._inline[:]
                self._inline = []
                self._is_inline = False
            self._heap.append(item)

    def pop(self) -> T | None:  # type: ignore
        if self._is_inline:
            if self._inline:
                return self._inline.pop()
            return None
        if self._heap:
            return self._heap.pop()
        return None

    def len(self) -> int:  # type: ignore
        return len(self._inline) + len(self._heap)

    def is_empty(self) -> bool:  # type: ignore
        return self.len() == 0

    def clear(self) -> None:  # type: ignore
        self._inline.clear()
        self._heap.clear()
        self._is_inline = True

    def as_slice(self) -> list[T]:  # type: ignore
        if self._is_inline:
            return self._inline[:]
        return self._heap[:]

    def into_vec(self) -> list[T]:  # type: ignore
        if self._is_inline:
            return self._inline
        return self._heap

    def retain(self, f: Callable[[T], bool]) -> None:  # type: ignore
        if self._is_inline:
            self._inline = [x for x in self._inline if f(x)]
        else:
            self._heap = [x for x in self._heap if f(x)]

    def __iter__(self) -> Iterator[T]:
        if self._is_inline:
            return iter(self._inline)
        return iter(self._heap)

    def __getitem__(self, index: int) -> T:
        if self._is_inline:
            return self._inline[index]
        return self._heap[index]

    def __setitem__(self, index: int, value: T) -> None:
        if self._is_inline:
            self._inline[index] = value
        else:
            self._heap[index] = value

    def __len__(self) -> int:
        return self.len()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        return f"TinyVec({self.as_slice()})"


class BitVec:
    __slots__ = ("_bits", "_len")

    def __init__(self, bits: Iterable[bool] | None = None) -> None:
        self._bits: list[bool] = list(bits) if bits else []
        self._len = len(self._bits)

    @classmethod
    def with_capacity(cls, capacity: int) -> BitVec:  # type: ignore
        v = cls()
        v._bits = [False] * capacity
        v._len = 0
        return v

    @classmethod
    def from_bytes(cls, data: bytes) -> BitVec:
        bits = []
        for byte in data:
            for i in range(8):
                bits.append(bool(byte & (1 << i)))
        return cls(bits)

    def push(self, bit: bool) -> None:
        self._bits.append(bit)
        self._len += 1

    def pop(self) -> bool | None:  # type: ignore
        if self._bits:
            self._len -= 1
            return self._bits.pop()
        return None

    def set(self, index: int, value: bool) -> None:  # type: ignore
        self._bits[index] = value

    def get(self, index: int) -> bool:  # type: ignore
        return self._bits[index]

    def flip(self, index: int) -> None:  # type: ignore
        self._bits[index] = not self._bits[index]

    def len(self) -> int:  # type: ignore
        return self._len

    def is_empty(self) -> bool:  # type: ignore
        return self._len == 0

    def capacity(self) -> int:  # type: ignore
        return len(self._bits)

    def clear(self) -> None:  # type: ignore
        self._bits.clear()
        self._len = 0

    def count_ones(self) -> int:  # type: ignore
        return sum(1 for b in self._bits if b)

    def count_zeros(self) -> int:  # type: ignore
        return sum(1 for b in self._bits if not b)

    def any(self) -> bool:  # type: ignore
        return any(self._bits)

    def all(self) -> bool:  # type: ignore
        return all(self._bits[:self._len])

    def to_bytes(self) -> bytes:  # type: ignore
        result = bytearray()
        for i in range(0, self._len, 8):
            byte = 0
            for j in range(8):
                if i + j < self._len and self._bits[i + j]:
                    byte |= 1 << j
            result.append(byte)
        return bytes(result)

    def as_slice(self) -> list[bool]:  # type: ignore
        return self._bits[:self._len]

    def __iter__(self) -> Iterator[bool]:
        return iter(self._bits[:self._len])

    def __getitem__(self, index: int) -> bool:
        return self._bits[index]

    def __setitem__(self, index: int, value: bool) -> None:
        self._bits[index] = value

    def __len__(self) -> int:
        return self._len

    def __bool__(self) -> bool:
        return self._len > 0

    def __repr__(self) -> str:
        return f"BitVec({self._len} bits)"


class Drain(Generic[T]):
    __slots__ = ("_source", "_index")

    def __init__(self, source: list[T]) -> None:
        self._source = source
        self._index = 0

    def __iter__(self) -> Iterator[T]:
        while self._index < len(self._source):
            yield self._source[self._index]
            self._index += 1
        self._source.clear()

    def __next__(self) -> T:
        if self._index >= len(self._source):
            raise StopIteration
        value = self._source[self._index]
        self._index += 1
        return value

    def __repr__(self) -> str:
        return f"Drain(remaining={len(self._source) - self._index})"


@dataclass(frozen=True, slots=True)
class CreateMeta:
    libname: str
    libversion: tuple[int, int]
    pyversion: tuple[int, int]
    author: str
    clone: str
    description: str
    license: str
    homepage: str
    keywords: tuple[str, ...]
    python_requires: str
    timestamp: str
    def unwrap(self) -> str:
        return self.libname
