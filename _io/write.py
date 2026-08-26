"""Write trait — byte and string writing."""
from __future__ import annotations

"""Write trait — writing abstraction.

Provides Write for byte/string writing with write, write_all, and flush.
"""

from typing import Any


class Write:
    def write(self, data: bytes | bytearray | str) -> int:  # type: ignore
        raise NotImplementedError

    def write_all(self, data: bytes | bytearray | str) -> None:  # type: ignore
        total = 0
        if isinstance(data, str):
            data = data.encode("utf-8")
        while total < len(data):
            n = self.write(data[total:])
            total += n

    def flush(self) -> None:  # type: ignore
        pass

    def by_ref(self) -> Any:  # type: ignore
        return self
