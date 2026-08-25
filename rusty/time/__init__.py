"""Time utilities — Duration, Instant, SystemTime, and UNIX_EPOCH."""
from __future__ import annotations

"""Time utilities — durations, timestamps, and wall-clock time.

Provides Duration, Instant, SystemTime, UNIX_EPOCH, and Elapsed.
"""

from .duration import Duration, UNIX_EPOCH, Elapsed
from .instant import Instant
from .system_time import SystemTime

__all__ = [
    "Duration",
    "UNIX_EPOCH",
    "Elapsed",
    "Instant",
    "SystemTime",
]
