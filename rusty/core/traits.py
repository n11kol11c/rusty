"""Trait protocols — 17 Rust-style traits (Clone, Debug, Display, From, Into, etc.) as Python protocols."""
from __future__ import annotations

"""Trait protocols — Rust-style traits as Python protocols.

Defines 17 trait protocols (Clone, Debug, Display, Default, From, Into, etc.)
and corresponding helper functions for polymorphic behavior.
"""

from typing import Any, Generic, Protocol, TypeVar, runtime_checkable

from .result import Result, Ok, Err


T = TypeVar("T")


@runtime_checkable
class CloneTrait(Protocol[T]):
    def clone(self) -> T: ...


@runtime_checkable
class CopyTrait(Protocol[T]):
    def copy(self) -> T: ...


@runtime_checkable
class DebugTrait(Protocol):
    def debug(self) -> str: ...


@runtime_checkable
class DisplayTrait(Protocol):
    def fmt(self) -> str: ...


@runtime_checkable
class DefaultTrait(Protocol[T]):
    @classmethod
    def default(cls) -> T: ...


@runtime_checkable
class EqTrait(Protocol):
    def eq(self, other: object) -> bool: ...
    def ne(self, other: object) -> bool: ...


@runtime_checkable
class OrdTrait(Protocol):
    def cmp(self, other: object) -> int: ...
    def lt(self, other: object) -> bool: ...
    def le(self, other: object) -> bool: ...
    def gt(self, other: object) -> bool: ...
    def ge(self, other: object) -> bool: ...


@runtime_checkable
class HashTrait(Protocol):
    def hash(self) -> int: ...


@runtime_checkable
class FromTrait(Protocol[T]):
    @classmethod
    def from_(cls, value: Any) -> T: ...


@runtime_checkable
class IntoTrait(Protocol[T]):
    def into(self) -> T: ...


@runtime_checkable
class TryFromTrait(Protocol[T]):
    @classmethod
    def try_from(cls, value: Any) -> Result[T, str]: ...


@runtime_checkable
class TryIntoTrait(Protocol[T]):
    def try_into(self) -> Result[T, str]: ...


@runtime_checkable
class AsRefTrait(Protocol[T]):
    def as_ref(self) -> T: ...


@runtime_checkable
class AsMutTrait(Protocol[T]):
    def as_mut(self) -> T: ...


@runtime_checkable
class DerefTrait(Protocol[T]):
    def deref(self) -> T: ...


@runtime_checkable
class DerefMutTrait(Protocol[T]):
    def deref_mut(self) -> T: ...


@runtime_checkable
class DropTrait(Protocol):
    def drop(self) -> None: ...


def clone(value: T) -> T:
    if hasattr(value, 'clone'):
        return value.clone()
    import copy as _copy
    return _copy.deepcopy(value)


def debug(value: Any) -> str:
    if hasattr(value, 'debug'):
        return value.debug()
    return repr(value)


def display(value: Any) -> str:
    if hasattr(value, 'fmt'):
        return value.fmt()
    return str(value)


def default_of(cls: type[T]) -> T:
    if hasattr(cls, 'default'):
        try:
            return cls.default()
        except TypeError:
            return cls.default(cls)
    return cls()


def from_(cls: type[T], value: Any) -> T:
    if hasattr(cls, 'from_'):
        return cls.from_(value)
    return cls(value)


def into(value: Any, target_type: type[T]) -> T:
    if hasattr(value, 'into'):
        return value.into()
    return target_type(value)


def try_from(cls: type[T], value: Any) -> Result[T, str]:
    if hasattr(cls, 'try_from'):
        return cls.try_from(value)
    try:
        return Ok(cls(value))
    except Exception as e:
        return Err(str(e))


def try_into(value: Any, target_type: type[T]) -> Result[T, str]:
    if hasattr(value, 'try_into'):
        return value.try_into()
    try:
        return Ok(target_type(value))
    except Exception as e:
        return Err(str(e))


def as_ref(value: T) -> T:
    if hasattr(value, 'as_ref'):
        return value.as_ref()
    return value


def as_mut(value: T) -> T:
    if hasattr(value, 'as_mut'):
        return value.as_mut()
    return value


def deref(value: T) -> T:
    if hasattr(value, 'deref'):
        return value.deref()
    return value


def deref_mut(value: T) -> T:
    if hasattr(value, 'deref_mut'):
        return value.deref_mut()
    return value


def drop(value: Any) -> None:
    if hasattr(value, 'drop'):
        value.drop()
