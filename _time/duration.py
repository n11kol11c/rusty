"""Duration — a span of time with arithmetic and comparisons."""
from __future__ import annotations

"""Duration — a span of time.

Provides Duration with from_secs, from_millis, from_nanos constructors
and arithmetic operations. Also defines UNIX_EPOCH and Elapsed.
"""


class Elapsed(Exception):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("timer expiration error")


class Duration:
    __slots__ = ("_secs", "_nanos")

    def __init__(self, secs: int = 0, nanos: int = 0) -> None:
        if secs < 0 or nanos < 0:
            raise ValueError("duration values must be non-negative")
        self._secs = secs + nanos // 1_000_000_000
        self._nanos = nanos % 1_000_000_000

    @classmethod
    def from_secs(cls, secs: int | float) -> Duration:
        s = int(secs)
        ns = int((secs - s) * 1_000_000_000)
        return cls(s, ns)

    @classmethod
    def from_millis(cls, millis: int | float) -> Duration:
        s = int(millis) // 1000
        ns = (int(millis) % 1000) * 1_000_000
        return cls(s, ns)

    @classmethod
    def from_micros(cls, micros: int | float) -> Duration:
        s = int(micros) // 1_000_000
        ns = (int(micros) % 1_000_000) * 1_000
        return cls(s, ns)

    @classmethod
    def from_nanos(cls, nanos: int) -> Duration:
        return cls(0, nanos)

    @classmethod
    def from_minutes(cls, minutes: int | float) -> Duration:
        return cls.from_secs(minutes * 60)

    @classmethod
    def from_hours(cls, hours: int | float) -> Duration:
        return cls.from_secs(hours * 3600)

    @classmethod
    def from_days(cls, days: int | float) -> Duration:
        return cls.from_secs(days * 86400)

    @classmethod
    def zero(cls) -> Duration:
        return cls(0, 0)

    def as_secs(self) -> int:
        return self._secs

    def as_millis(self) -> int:
        return self._secs * 1000 + self._nanos // 1_000_000

    def as_micros(self) -> int:
        return self._secs * 1_000_000 + self._nanos // 1_000

    def as_nanos(self) -> int:
        return self._secs * 1_000_000_000 + self._nanos

    def secs_f64(self) -> float:
        return self._secs + self._nanos / 1_000_000_000

    def is_zero(self) -> bool:
        return self._secs == 0 and self._nanos == 0

    def checked_add(self, other: Duration) -> Duration | None:
        try:
            return Duration(self._secs + other._secs, self._nanos + other._nanos)
        except (ValueError, OverflowError):
            return None

    def checked_sub(self, other: Duration) -> Duration | None:
        total_self = self.as_nanos()
        total_other = other.as_nanos()
        if total_self < total_other:
            return None
        return Duration.from_nanos(total_self - total_other)

    def saturating_add(self, other: Duration) -> Duration:
        result = self.checked_add(other)
        return result if result else Duration.from_secs(float('inf'))

    def saturating_sub(self, other: Duration) -> Duration:
        result = self.checked_sub(other)
        return result if result else Duration.zero()

    def mul(self, rhs: int) -> Duration:
        return Duration.from_nanos(self.as_nanos() * rhs)

    def div(self, rhs: int) -> Duration:
        if rhs == 0:
            raise ZeroDivisionError("division by zero")
        return Duration.from_nanos(self.as_nanos() // rhs)

    def __add__(self, other: Duration) -> Duration:
        return Duration(self._secs + other._secs, self._nanos + other._nanos)

    def __sub__(self, other: Duration) -> Duration:
        result = self.checked_sub(other)
        if result is None:
            raise ValueError("underflow in duration subtraction")
        return result

    def __mul__(self, rhs: int) -> Duration:
        return self.mul(rhs)

    def __rmul__(self, lhs: int) -> Duration:
        return self.mul(lhs)

    def __floordiv__(self, rhs: int) -> Duration:
        return self.div(rhs)

    def __mod__(self, other: Duration) -> Duration:
        nanos = self.as_nanos() % other.as_nanos()
        return Duration.from_nanos(nanos)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Duration):
            return self._secs == other._secs and self._nanos == other._nanos
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Duration):
            return self._secs != other._secs or self._nanos != other._nanos
        return NotImplemented

    def __lt__(self, other: Duration) -> bool:
        if isinstance(other, Duration):
            return self.as_nanos() < other.as_nanos()
        return NotImplemented

    def __le__(self, other: Duration) -> bool:
        if isinstance(other, Duration):
            return self.as_nanos() <= other.as_nanos()
        return NotImplemented

    def __gt__(self, other: Duration) -> bool:
        if isinstance(other, Duration):
            return self.as_nanos() > other.as_nanos()
        return NotImplemented

    def __ge__(self, other: Duration) -> bool:
        if isinstance(other, Duration):
            return self.as_nanos() >= other.as_nanos()
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._secs, self._nanos))

    def __repr__(self) -> str:
        if self._nanos == 0:
            return f"Duration(secs={self._secs})"
        return f"Duration(secs={self._secs}, nanos={self._nanos})"

    def __bool__(self) -> bool:
        return not self.is_zero()


UNIX_EPOCH = Duration(0, 0)
