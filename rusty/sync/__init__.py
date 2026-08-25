"""Synchronization primitives — Atomic, Mutex, RwLock, Channel, Barrier, and more."""
from __future__ import annotations
"""Synchronization primitives for concurrent programming.

Provides Atomic types, Mutex, RwLock, Barrier, Condvar, Channel (MPSC),
Once, and Semaphore for safe multi-threaded coordination.
"""

from rusty.sync.atomic import Atomic, AtomicBool, AtomicInt
from rusty.sync.mutex import Mutex, MutexGuard
from rusty.sync.rwlock import RwLock, RwLockReadGuard, RwLockWriteGuard
from rusty.sync.arc import Arc
from rusty.sync.barrier import Barrier
from rusty.sync.condvar import Condvar
from rusty.sync.channel import Channel, Sender, Receiver
from rusty.sync.once import Once
from rusty.sync.semaphore import Semaphore

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
