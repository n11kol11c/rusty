"""Ipv4Addr, Ipv6Addr, IpAddr, SocketAddr, Shutdown — network addresses."""
from __future__ import annotations

"""Address types — IP addresses and socket addresses.

Provides Ipv4Addr, Ipv6Addr, IpAddr, SocketAddr, and Shutdown
for network addressing.
"""


class Shutdown:
    __slots__ = ("_kind",)

    READ = 0
    WRITE = 1
    BOTH = 2

    def __init__(self, kind: int) -> None:
        self._kind = kind

    @classmethod
    def read(cls) -> Shutdown:
        return cls(cls.READ)

    @classmethod
    def write(cls) -> Shutdown:
        return cls(cls.WRITE)

    @classmethod
    def both(cls) -> Shutdown:
        return cls(cls.BOTH)

    def kind(self) -> int:
        return self._kind

    def __repr__(self) -> str:
        if self._kind == self.READ:
            return "Shutdown::Read"
        if self._kind == self.WRITE:
            return "Shutdown::Write"
        return "Shutdown::Both"


class Ipv4Addr:
    __slots__ = ("_octets",)

    def __init__(self, a: int = 0, b: int = 0, c: int = 0, d: int = 0) -> None:
        self._octets = (a, b, c, d)

    @classmethod
    def new(cls, a: int, b: int, c: int, d: int) -> Ipv4Addr:  # type: ignore
        return cls(a, b, c, d)

    @classmethod
    def from_str(cls, s: str) -> Ipv4Addr:  # type: ignore
        parts = s.split(".")
        if len(parts) != 4:
            raise ValueError(f"invalid IPv4 address: {s}")
        return cls(*[int(p) for p in parts])

    @classmethod
    def from_bytes(cls, bytes: bytes | bytearray) -> Ipv4Addr:  # type: ignore
        if len(bytes) != 4:
            raise ValueError("IPv4 address must be 4 bytes")
        return cls(bytes[0], bytes[1], bytes[2], bytes[3])

    @classmethod
    def localhost(cls) -> Ipv4Addr:  # type: ignore
        return cls(127, 0, 0, 1)

    @classmethod
    def unspecified(cls) -> Ipv4Addr:  # type: ignore
        return cls(0, 0, 0, 0)

    @classmethod
    def broadcast(cls) -> Ipv4Addr:  # type: ignore
        return cls(255, 255, 255, 255)

    @classmethod
    def loopback(cls) -> Ipv4Addr:  # type: ignore
        return cls(127, 0, 0, 1)

    def octets(self) -> tuple[int, int, int, int]:
        return self._octets

    def to_str(self) -> str:  # type: ignore
        return ".".join(str(o) for o in self._octets)

    def to_bytes(self) -> bytes:  # type: ignore
        return bytes(self._octets)

    def is_loopback(self) -> bool:  # type: ignore
        return self._octets[0] == 127

    def is_unspecified(self) -> bool:  # type: ignore
        return self._octets == (0, 0, 0, 0)

    def is_broadcast(self) -> bool:  # type: ignore
        return self._octets == (255, 255, 255, 255)

    def is_multicast(self) -> bool:  # type: ignore
        return (self._octets[0] & 0xF0) == 0xE0

    def is_private(self) -> bool:  # type: ignore
        return (
            self._octets[0] == 10
            or (self._octets[0] == 172 and 16 <= self._octets[1] <= 31)
            or (self._octets[0] == 192 and self._octets[1] == 168)
        )

    def is_link_local(self) -> bool:  # type: ignore
        return self._octets[0] == 169 and self._octets[1] == 254

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ipv4Addr):
            return self._octets == other._octets
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Ipv4Addr):
            return self._octets != other._octets
        return NotImplemented

    def __lt__(self, other: Ipv4Addr) -> bool:
        if isinstance(other, Ipv4Addr):
            return self._octets < other._octets
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._octets)

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"Ipv4Addr({self.to_str()!r})"


class Ipv6Addr:
    __slots__ = ("_segments",)

    def __init__(self, *segments: int) -> None:
        if len(segments) == 0:
            self._segments = (0,) * 8
        elif len(segments) == 8:
            self._segments = tuple(segments)
        else:
            raise ValueError("IPv6 address must have 0 or 8 segments")

    @classmethod
    def new(cls, a: int, b: int, c: int, d: int, e: int, f: int, g: int, h: int) -> Ipv6Addr:  # type: ignore
        return cls(a, b, c, d, e, f, g, h)

    @classmethod
    def from_str(cls, s: str) -> Ipv6Addr:  # type: ignore
        import ipaddress
        addr = ipaddress.IPv6Address(s)
        b = addr.packed
        segments = []
        for i in range(0, 16, 2):
            segments.append((b[i] << 8) | b[i + 1])
        return cls(*segments)

    @classmethod
    def from_bytes(cls, data: bytes | bytearray) -> Ipv6Addr:  # type: ignore
        if len(data) != 16:
            raise ValueError("IPv6 address must be 16 bytes")
        segments = []
        for i in range(0, 16, 2):
            segments.append((data[i] << 8) | data[i + 1])
        return cls(*segments)

    @classmethod
    def localhost(cls) -> Ipv6Addr:  # type: ignore
        return cls(0, 0, 0, 0, 0, 0, 0, 1)

    @classmethod
    def unspecified(cls) -> Ipv6Addr:  # type: ignore
        return cls(0, 0, 0, 0, 0, 0, 0, 0)

    @classmethod
    def loopback(cls) -> Ipv6Addr:  # type: ignore
        return cls(0, 0, 0, 0, 0, 0, 0, 1)

    @classmethod
    def multicast(cls, scope: int = 2) -> Ipv6Addr:  # type: ignore
        return cls(0xFF00 | scope, 0, 0, 0, 0, 0, 0, 0)

    @classmethod
    def link_local(cls) -> Ipv6Addr:  # type: ignore
        return cls(0xFE80, 0, 0, 0, 0, 0, 0, 0x0001)

    def segments(self) -> tuple[int, ...]:
        return self._segments

    def to_str(self) -> str:  # type: ignore
        import ipaddress
        b = bytearray(16)
        for i, seg in enumerate(self._segments):
            b[i * 2] = seg >> 8
            b[i * 2 + 1] = seg & 0xFF
        return str(ipaddress.IPv6Address(bytes(b)))

    def to_bytes(self) -> bytes:  # type: ignore
        b = bytearray(16)
        for i, seg in enumerate(self._segments):
            b[i * 2] = seg >> 8
            b[i * 2 + 1] = seg & 0xFF
        return bytes(b)

    def is_loopback(self) -> bool:  # type: ignore
        return self._segments == (0, 0, 0, 0, 0, 0, 0, 1)

    def is_unspecified(self) -> bool:  # type: ignore
        return self._segments == (0, 0, 0, 0, 0, 0, 0, 0)

    def is_multicast(self) -> bool:  # type: ignore
        return (self._segments[0] & 0xFF00) == 0xFF00

    def is_unicast_link_local(self) -> bool:  # type: ignore
        return (self._segments[0] & 0xFFC0) == 0xFE80

    def to_ipv4_mapped(self) -> Ipv4Addr:  # type: ignore
        if self._segments[0] == 0 and self._segments[1] == 0 and self._segments[2] == 0 and self._segments[3] == 0 and self._segments[4] == 0:
            return Ipv4Addr(
                (self._segments[6] >> 8) & 0xFF,
                self._segments[6] & 0xFF,
                (self._segments[7] >> 8) & 0xFF,
                self._segments[7] & 0xFF,
            )
        raise ValueError("not an IPv4-mapped address")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ipv6Addr):
            return self._segments == other._segments
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Ipv6Addr):
            return self._segments != other._segments
        return NotImplemented

    def __lt__(self, other: Ipv6Addr) -> bool:
        if isinstance(other, Ipv6Addr):
            return self._segments < other._segments
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._segments)

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"Ipv6Addr({self.to_str()!r})"


class IpAddr:
    __slots__ = ("_v4", "_v6")

    def __init__(self, v4: Ipv4Addr | None = None, v6: Ipv6Addr | None = None) -> None:
        if v4 is not None and v6 is not None:
            raise ValueError("IpAddr cannot be both v4 and v6")
        self._v4 = v4
        self._v6 = v6

    @classmethod
    def v4(cls, addr: Ipv4Addr) -> IpAddr:
        return cls(v4=addr)

    @classmethod
    def v6(cls, addr: Ipv6Addr) -> IpAddr:
        return cls(v6=addr)

    @classmethod
    def from_str(cls, s: str) -> IpAddr:
        try:
            return cls.v4(Ipv4Addr.from_str(s))
        except ValueError:
            pass
        return cls.v6(Ipv6Addr.from_str(s))

    def is_ipv4(self) -> bool:  # type: ignore
        return self._v4 is not None

    def is_ipv6(self) -> bool:  # type: ignore
        return self._v6 is not None

    def as_ipv4(self) -> Ipv4Addr | None:
        return self._v4

    def as_ipv6(self) -> Ipv6Addr | None:  # type: ignore
        return self._v6

    def to_ipv4(self) -> Ipv4Addr | None:  # type: ignore
        return self._v4

    def to_ipv6(self) -> Ipv6Addr | None:  # type: ignore
        return self._v6

    def is_loopback(self) -> bool:  # type: ignore
        if self._v4:
            return self._v4.is_loopback()
        if self._v6:
            return self._v6.is_loopback()
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, IpAddr):
            return self._v4 == other._v4 and self._v6 == other._v6
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, IpAddr):
            return self._v4 != other._v4 or self._v6 != other._v6
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._v4, self._v6))

    def __str__(self) -> str:
        if self._v4:
            return str(self._v4)
        return str(self._v6)

    def __repr__(self) -> str:
        if self._v4:
            return f"IpAddr::V4({self._v4!r})"
        return f"IpAddr::V6({self._v6!r})"


class SocketAddr:
    __slots__ = ("_ip", "_port")

    def __init__(self, ip: IpAddr, port: int) -> None:
        self._ip = ip
        self._port = port

    @classmethod
    def new(cls, ip: IpAddr, port: int) -> SocketAddr:
        return cls(ip, port)

    @classmethod
    def from_str(cls, s: str) -> SocketAddr:
        if s.startswith("["):
            bracket = s.find("]")
            if bracket < 0:
                raise ValueError(f"invalid socket address: {s}")
            ip_str = s[1:bracket]
            rest = s[bracket + 1:]
            if not rest.startswith(":"):
                raise ValueError(f"invalid socket address: {s}")
            port = int(rest[1:])
            return cls(IpAddr.v6(Ipv6Addr.from_str(ip_str)), port)
        colon = s.rfind(":")
        if colon < 0:
            raise ValueError(f"invalid socket address: {s}")
        ip_str = s[:colon]
        port = int(s[colon + 1:])
        return cls(IpAddr.from_str(ip_str), port)

    @classmethod
    def new_v4(cls, ip: Ipv4Addr, port: int) -> SocketAddr:
        return cls(IpAddr.v4(ip), port)

    @classmethod
    def new_v6(cls, ip: Ipv6Addr, port: int) -> SocketAddr:
        return cls(IpAddr.v6(ip), port)

    def ip(self) -> IpAddr:  # type: ignore
        return self._ip

    def port(self) -> int:
        return self._port

    def is_ipv4(self) -> bool:  # type: ignore
        return self._ip.is_ipv4()

    def is_ipv6(self) -> bool:  # type: ignore
        return self._ip.is_ipv6()

    def set_ip(self, ip: IpAddr) -> None:
        self._ip = ip

    def set_port(self, port: int) -> None:  # type: ignore
        self._port = port

    def to_socket_addr(self) -> tuple[str, int]:  # type: ignore
        return (str(self._ip), self._port)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SocketAddr):
            return self._ip == other._ip and self._port == other._port
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, SocketAddr):
            return self._ip != other._ip or self._port != other._port
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._ip, self._port))

    def __str__(self) -> str:
        if self._ip.is_ipv6():
            return f"[{self._ip}]:{self._port}"
        return f"{self._ip}:{self._port}"

    def __repr__(self) -> str:
        return f"SocketAddr({self})"
