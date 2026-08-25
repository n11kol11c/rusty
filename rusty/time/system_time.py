"""SystemTime — wall-clock time with datetime conversion."""
from __future__ import annotations

"""SystemTime — wall-clock time.

Provides SystemTime for calendar time operations, conversion to
datetime, and computing durations since the Unix epoch.
"""

import datetime as _dt_module

from .duration import Duration, Elapsed


class SystemTime:
    __slots__ = ("_seconds", "_nanos", "_tz")

    def __init__(self) -> None:
        now = _dt_module.datetime.now()
        epoch = _dt_module.datetime(1970, 1, 1)
        delta = now - epoch
        self._seconds = int(delta.total_seconds())
        self._nanos = delta.microseconds * 1000
        self._tz = now.tzinfo

    @classmethod
    def now(cls) -> SystemTime:
        return cls()

    @classmethod
    def from_secs(cls, secs: int, nanos: int = 0) -> SystemTime:
        t = cls.__new__(cls)
        t._seconds = secs
        t._nanos = nanos
        t._tz = None
        return t

    def duration_since(self, earlier: SystemTime) -> Duration:
        diff_secs = self._seconds - earlier._seconds
        diff_nanos = self._nanos - earlier._nanos
        if diff_nanos < 0:
            diff_secs -= 1
            diff_nanos += 1_000_000_000
        if diff_secs < 0:
            raise Elapsed()
        return Duration(diff_secs, diff_nanos)

    def checked_duration_since(self, earlier: SystemTime) -> Duration | None:
        diff_secs = self._seconds - earlier._seconds
        diff_nanos = self._nanos - earlier._nanos
        if diff_nanos < 0:
            diff_secs -= 1
            diff_nanos += 1_000_000_000
        if diff_secs < 0:
            return None
        return Duration(diff_secs, diff_nanos)

    def saturating_duration_since(self, earlier: SystemTime) -> Duration:
        result = self.checked_duration_since(earlier)
        return result if result else Duration.zero()

    def add_duration(self, duration: Duration) -> SystemTime:
        new_secs = self._seconds + duration._secs
        new_nanos = self._nanos + duration._nanos
        if new_nanos >= 1_000_000_000:
            new_secs += 1
            new_nanos -= 1_000_000_000
        t = SystemTime.__new__(SystemTime)
        t._seconds = new_secs
        t._nanos = new_nanos
        t._tz = None
        return t

    def checked_add_duration(self, duration: Duration) -> SystemTime | None:
        try:
            return self.add_duration(duration)
        except (ValueError, OverflowError):
            return None

    def checked_sub_duration(self, duration: Duration) -> SystemTime | None:
        new_secs = self._seconds - duration._secs
        new_nanos = self._nanos - duration._nanos
        if new_nanos < 0:
            new_secs -= 1
            new_nanos += 1_000_000_000
        if new_secs < 0:
            return None
        t = SystemTime.__new__(SystemTime)
        t._seconds = new_secs
        t._nanos = new_nanos
        t._tz = None
        return t

    def sub(self, other: SystemTime) -> Duration:
        return self.duration_since(other)

    def as_secs(self) -> int:
        return self._seconds

    def from_epoch(self) -> Duration:
        return Duration(self._seconds, self._nanos)

    def to_datetime(self) -> _dt_module.datetime:
        return _dt_module.datetime.fromtimestamp(self._seconds, tz=self._tz)

    def __sub__(self, other: SystemTime) -> Duration:
        return self.duration_since(other)

    def __add__(self, duration: Duration) -> SystemTime:
        return self.add_duration(duration)

    def __radd__(self, duration: Duration) -> SystemTime:
        return self.add_duration(duration)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SystemTime):
            return self._seconds == other._seconds and self._nanos == other._nanos
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, SystemTime):
            return self._seconds != other._seconds or self._nanos != other._nanos
        return NotImplemented

    def __lt__(self, other: SystemTime) -> bool:
        if isinstance(other, SystemTime):
            return (self._seconds, self._nanos) < (other._seconds, other._nanos)
        return NotImplemented

    def __le__(self, other: SystemTime) -> bool:
        if isinstance(other, SystemTime):
            return (self._seconds, self._nanos) <= (other._seconds, other._nanos)
        return NotImplemented

    def __gt__(self, other: SystemTime) -> bool:
        if isinstance(other, SystemTime):
            return (self._seconds, self._nanos) > (other._seconds, other._nanos)
        return NotImplemented

    def __ge__(self, other: SystemTime) -> bool:
        if isinstance(other, SystemTime):
            return (self._seconds, self._nanos) >= (other._seconds, other._nanos)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._seconds, self._nanos))

    def __repr__(self) -> str:
        return f"SystemTime({self._seconds}.{self._nanos:09d})"
