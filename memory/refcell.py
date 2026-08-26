"""RefCell — runtime borrow-checked interior mutability with Ref/RefMut guards."""
from __future__ import annotations
"""RefCell — runtime borrow-checked interior mutability.

Provides RefCell[T] with Ref and RefMut guards for single-threaded
interior mutability with runtime borrow checking.
"""

from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BorrowError(Exception):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("already mutably borrowed")


class BorrowMutError(Exception):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("already borrowed")


class RefCell(Generic[T]):
    __slots__ = ("_value", "_borrow_count")

    def __init__(self, value: T) -> None:
        self._value = value
        self._borrow_count = 0

    @classmethod
    def new(cls, value: T) -> RefCell[T]:
        return cls(value)

    def borrow(self) -> Ref[T]:
        if self._borrow_count < 0:
            raise BorrowError()
        self._borrow_count += 1
        return Ref(self)

    def try_borrow(self) -> Ref[T] | None:
        if self._borrow_count < 0:
            return None
        self._borrow_count += 1
        return Ref(self)

    def borrow_mut(self) -> RefMut[T]:
        if self._borrow_count != 0:
            raise BorrowMutError()
        self._borrow_count = -1
        return RefMut(self)

    def try_borrow_mut(self) -> RefMut[T] | None:
        if self._borrow_count != 0:
            return None
        self._borrow_count = -1
        return RefMut(self)

    def replace(self, value: T) -> T:
        old = self._value
        self._value = value
        return old

    def swap(self, other: RefCell[T]) -> None:
        self._value, other._value = other._value, self._value

    def into_inner(self) -> T:
        return self._value

    def _release_borrow(self) -> None:
        if self._borrow_count == -1:
            self._borrow_count = 0
        elif self._borrow_count > 0:
            self._borrow_count -= 1

    def __repr__(self) -> str:
        return f"RefCell({self._value!r})"


class Ref(Generic[T]):
    __slots__ = ("_cell",)

    def __init__(self, cell: RefCell) -> None:
        self._cell = cell

    @property
    def value(self) -> Any:
        return self._cell._value

    def release(self) -> None:
        self._cell._release_borrow()

    def __enter__(self) -> Ref[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __eq__(self, other: Any) -> bool:
        return self._cell._value == other

    def __ne__(self, other: Any) -> bool:
        return self._cell._value != other

    def __lt__(self, other: Any) -> bool:
        return self._cell._value < other

    def __le__(self, other: Any) -> bool:
        return self._cell._value <= other

    def __gt__(self, other: Any) -> bool:
        return self._cell._value > other

    def __ge__(self, other: Any) -> bool:
        return self._cell._value >= other

    def __hash__(self) -> int:
        return hash(self._cell._value)

    def __bool__(self) -> bool:
        return bool(self._cell._value)

    def __int__(self) -> int:
        return int(self._cell._value)

    def __float__(self) -> float:
        return float(self._cell._value)

    def __str__(self) -> str:
        return str(self._cell._value)

    def __repr__(self) -> str:
        return f"Ref({self._cell._value!r})"


class RefMut(Generic[T]):
    __slots__ = ("_cell",)

    def __init__(self, cell: RefCell) -> None:
        self._cell = cell

    @property
    def value(self) -> Any:
        return self._cell._value

    @value.setter
    def value(self, v: Any) -> None:
        self._cell._value = v

    def replace(self, v: Any) -> Any:
        old = self._cell._value
        self._cell._value = v
        return old

    def release(self) -> None:
        self._cell._release_borrow()

    def __enter__(self) -> RefMut[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __eq__(self, other: Any) -> bool:
        return self._cell._value == other

    def __ne__(self, other: Any) -> bool:
        return self._cell._value != other

    def __lt__(self, other: Any) -> bool:
        return self._cell._value < other

    def __le__(self, other: Any) -> bool:
        return self._cell._value <= other

    def __gt__(self, other: Any) -> bool:
        return self._cell._value > other

    def __ge__(self, other: Any) -> bool:
        return self._cell._value >= other

    def __hash__(self) -> int:
        return hash(self._cell._value)

    def __bool__(self) -> bool:
        return bool(self._cell._value)

    def __int__(self) -> int:
        return int(self._cell._value)

    def __float__(self) -> float:
        return float(self._cell._value)

    def __str__(self) -> str:
        return str(self._cell._value)

    def __repr__(self) -> str:
        return f"RefMut({self._cell._value!r})"
