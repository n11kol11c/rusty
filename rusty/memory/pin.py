"""Pin, ManuallyDrop, MaybeUninit, NonNull, PhantomData — low-level memory primitives."""
from __future__ import annotations
"""Pin and related types — pinned references and low-level primitives.

Provides Pin for pinning values in memory, ManuallyDrop for controlling
destruction, MaybeUninit for uninitialized memory, NonNull for non-null
pointers, PhantomData for type-level markers, and Borrow/BorrowMut traits.
"""

from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Pin(Generic[T]):
    __slots__ = ("_value", "_pinned")

    def __init__(self, value: T) -> None:
        self._value = value
        self._pinned = True

    @classmethod
    def new(cls, value: T) -> Pin[T]:
        return cls(value)

    @classmethod
    def into_pin(cls, value: T) -> Pin[T]:
        return cls(value)

    def as_ref(self) -> T:
        return self._value

    def as_mut(self) -> T:
        return self._value

    def into_inner(self) -> T:
        self._pinned = False
        return self._value

    def is_pinned(self) -> bool:
        return self._pinned

    def __repr__(self) -> str:
        return f"Pin({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pin):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __enter__(self) -> Pin[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass


class ManuallyDrop(Generic[T]):
    __slots__ = ("_value", "_dropped")

    def __init__(self, value: T) -> None:
        self._value = value
        self._dropped = False

    @classmethod
    def new(cls, value: T) -> ManuallyDrop[T]:
        return cls(value)

    def as_ref(self) -> T:
        return self._value

    def as_mut(self) -> T:
        return self._value

    def into_inner(self) -> T:
        self._dropped = True
        return self._value

    def drop(self) -> None:
        self._dropped = True
        self._value = None  # type: ignore[assignment]

    def is_dropped(self) -> bool:
        return self._dropped

    def __repr__(self) -> str:
        return f"ManuallyDrop({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ManuallyDrop):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __del__(self) -> None:
        if not self._dropped:
            self._dropped = True


class MaybeUninit(Generic[T]):
    __slots__ = ("_value", "_initialized")

    def __init__(self) -> None:
        self._value: T = None  # type: ignore[assignment]
        self._initialized = False

    @classmethod
    def new(cls) -> MaybeUninit[T]:
        return cls()

    @classmethod
    def uninit(cls) -> MaybeUninit[T]:
        return cls()

    @classmethod
    def init(cls, value: T) -> MaybeUninit[T]:
        cell = cls()
        cell._value = value
        cell._initialized = True
        return cell

    def assume_init(self) -> T:
        if not self._initialized:
            raise ValueError("MaybeUninit is not initialized")
        return self._value

    def write(self, value: T) -> T:
        self._value = value
        self._initialized = True
        return value

    def as_ptr(self) -> int:
        return id(self._value)

    def is_initialized(self) -> bool:
        return self._initialized

    def __repr__(self) -> str:
        if self._initialized:
            return f"MaybeUninit({self._value!r})"
        return "MaybeUninit(<uninitialized>)"

    def __bool__(self) -> bool:
        return self._initialized

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MaybeUninit):
            if not self._initialized or not other._initialized:
                return False
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        if self._initialized:
            return hash(self._value)
        return hash(None)


class NonNull(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        if value is None:
            raise ValueError("NonNull cannot hold None")
        self._value = value

    @classmethod
    def new(cls, value: T) -> NonNull[T]:
        return cls(value)

    def as_ref(self) -> T:
        return self._value

    def as_mut(self) -> T:
        return self._value

    def replace(self, value: T) -> T:
        if value is None:
            raise ValueError("NonNull cannot hold None")
        old = self._value
        self._value = value
        return old

    def into_inner(self) -> T:
        return self._value

    def is_null(self) -> bool:
        return False

    def as_ptr(self) -> int:
        return id(self._value)

    def __repr__(self) -> str:
        return f"NonNull({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NonNull):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return True


class PhantomData(Generic[T]):
    __slots__ = ()

    def __init__(self) -> None:
        pass

    @classmethod
    def new(cls) -> PhantomData[T]:
        return cls()

    def __repr__(self) -> str:
        return "PhantomData"

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PhantomData)

    def __hash__(self) -> int:
        return 0


class Borrow(Generic[T]):
    __slots__ = ("_value", "_owner")

    def __init__(self, value: T, owner: Any = None) -> None:
        self._value = value
        self._owner = owner

    @classmethod
    def new(cls, value: T, owner: Any = None) -> Borrow[T]:
        return cls(value, owner)

    def as_ref(self) -> T:
        return self._value

    def into_inner(self) -> T:
        return self._value

    def __repr__(self) -> str:
        return f"Borrow({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Borrow):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __enter__(self) -> Borrow[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass


class BorrowMut(Generic[T]):
    __slots__ = ("_value", "_owner", "_released")

    def __init__(self, value: T, owner: Any = None) -> None:
        self._value = value
        self._owner = owner
        self._released = False

    @classmethod
    def new(cls, value: T, owner: Any = None) -> BorrowMut[T]:
        return cls(value, owner)

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, v: T) -> None:
        self._value = v

    def replace(self, v: T) -> T:
        old = self._value
        self._value = v
        return old

    def into_inner(self) -> T:
        self._released = True
        return self._value

    def release(self) -> None:
        self._released = True

    def is_released(self) -> bool:
        return self._released

    def __enter__(self) -> BorrowMut[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"BorrowMut({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BorrowMut):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)
