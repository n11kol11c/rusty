"""Synchronization primitives — Atomic, Mutex, RwLock, Channel, Barrier, and more."""
from __future__ import annotations
"""Synchronization primitives for concurrent programming.

Provides Atomic types, Mutex, RwLock, Barrier, Condvar, Channel (MPSC),
Once, and Semaphore for safe multi-threaded coordination.
"""

from .atomic import Atomic, AtomicBool, AtomicInt
from .mutex import Mutex, MutexGuard
from .rwlock import RwLock, RwLockReadGuard, RwLockWriteGuard
from .arc import Arc
from .barrier import Barrier
from .condvar import Condvar
from .channel import Channel, Sender, Receiver
from .once import Once
from .semaphore import Semaphore

__all__ = [
    "Atomic",
    "AtomicBool",
    "AtomicInt",
    "Mutex",
    "MutexGuard",
    "Arc",
    "RwLock",
    "RwLockReadGuard",
    "RwLockWriteGuard",
    "Barrier",
    "Condvar",
    "Channel",
    "Sender",
    "Receiver",
    "Once",
    "Semaphore",
]
