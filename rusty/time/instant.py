"""Instant — a monotonic timestamp for measuring elapsed time."""
from __future__ import annotations

"""Instant — a monotonic timestamp.

Provides Instant for measuring elapsed time and computing durations
between points. Uses monotonic clock for reliability.
"""

import time

from .duration import Duration, Elapsed


class Instant:
    __slots__ = ("_monotonic", "_wall")

    def __init__(self) -> None:
        self._monotonic = time.monotonic()
        self._wall = time.time()

    @classmethod
    def now(cls) -> Instant:
        return cls()

    @classmethod
    def from_secs(cls, secs: float) -> Instant:
        inst = cls()
        inst._wall = secs
        return inst

    def elapsed(self) -> Duration:
        return Duration.from_secs(time.monotonic() - self._monotonic)

    def checked_elapsed(self) -> Duration | None:
        diff = time.monotonic() - self._monotonic
        if diff < 0:
            return None
        return Duration.from_secs(diff)

    def checked_duration_since(self, earlier: Instant) -> Duration | None:
        diff = self._monotonic - earlier._monotonic
        if diff < 0:
            return None
        return Duration.from_secs(diff)

    def duration_since(self, earlier: Instant) -> Duration:
        diff = self._monotonic - earlier._monotonic
        if diff < 0:
            raise Elapsed()
        return Duration.from_secs(diff)

    def checked_since(self, earlier: Instant) -> Instant | None:
        diff = self._monotonic - earlier._monotonic
        if diff < 0:
            return None
        return self

    def saturating_duration_since(self, earlier: Instant) -> Duration:
        diff = self._monotonic - earlier._monotonic
        if diff < 0:
            return Duration.zero()
        return Duration.from_secs(diff)

    def add_duration(self, duration: Duration) -> Instant:
        inst = Instant()
        inst._monotonic = self._monotonic + duration.secs_f64()
        inst._wall = self._wall + duration.secs_f64()
        return inst

    def checked_add_duration(self, duration: Duration) -> Instant | None:
        try:
            return self.add_duration(duration)
        except (ValueError, OverflowError):
            return None

    def as_secs(self) -> float:
        return self._wall

    def as_millis(self) -> int:
        return int(self._wall * 1000)

    def __sub__(self, other: Instant) -> Duration:
        return self.duration_since(other)

    def __add__(self, duration: Duration) -> Instant:
        return self.add_duration(duration)

    def __radd__(self, duration: Duration) -> Instant:
        return self.add_duration(duration)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Instant):
            return self._monotonic == other._monotonic
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Instant):
            return self._monotonic != other._monotonic
        return NotImplemented

    def __lt__(self, other: Instant) -> bool:
        if isinstance(other, Instant):
            return self._monotonic < other._monotonic
        return NotImplemented

    def __le__(self, other: Instant) -> bool:
        if isinstance(other, Instant):
            return self._monotonic <= other._monotonic
        return NotImplemented

    def __gt__(self, other: Instant) -> bool:
        if isinstance(other, Instant):
            return self._monotonic > other._monotonic
        return NotImplemented

    def __ge__(self, other: Instant) -> bool:
        if isinstance(other, Instant):
            return self._monotonic >= other._monotonic
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._monotonic)

    def __repr__(self) -> str:
        return f"Instant({self._wall:.6f})"
