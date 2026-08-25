"""UdpSocket — UDP datagram socket."""
from __future__ import annotations

"""UDP networking — datagram sockets.

Provides UdpSocket for send_to, recv_from, and connected UDP operations.
"""

import os
from typing import Any

from .address import SocketAddr


class UdpSocket:
    __slots__ = ("_socket", "_addr")

    def __init__(self, sock: Any, addr: SocketAddr | None = None) -> None:
        self._socket = sock
        self._addr = addr

    @classmethod
    def bind(cls, addr: SocketAddr) -> UdpSocket:
        import socket
        sock = socket.socket(
            socket.AF_INET if addr.is_ipv4() else socket.AF_INET6,
            socket.SOCK_DGRAM,
        )
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addr.to_socket_addr())
        return UdpSocket(sock, addr)

    @classmethod
    def from_std(cls, socket: Any, addr: SocketAddr | None = None) -> UdpSocket:
        return UdpSocket(socket, addr)

    def local_addr(self) -> SocketAddr | None:  # type: ignore
        if self._socket:
            try:
                addr = self._socket.getsockname()
                return SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
            except Exception:
                pass
        return None

    def send_to(self, buf: bytes | bytearray, target: SocketAddr) -> int:  # type: ignore
        return self._socket.sendto(buf, target.to_socket_addr())  # type: ignore

    def recv_from(self, buf_size: int) -> tuple[bytes, SocketAddr]:  # type: ignore
        data, addr = self._socket.recvfrom(buf_size)  # type: ignore
        sock_addr = SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
        return data, sock_addr

    def recv(self, buf_size: int) -> bytes:  # type: ignore
        return self._socket.recv(buf_size)  # type: ignore

    def send(self, data: bytes | bytearray) -> int:  # type: ignore
        return self._socket.send(data)  # type: ignore

    def connect(self, addr: SocketAddr) -> None:  # type: ignore
        self._socket.connect(addr.to_socket_addr())  # type: ignore
        self._addr = addr

    def set_broadcast(self, on: bool) -> None:  # type: ignore
        self._socket.setsockopt(
            __import__('socket').SOL_SOCKET,
            __import__('socket').SO_BROADCAST,
            1 if on else 0,
        )

    def set_nonblocking(self, nonblocking: bool) -> None:  # type: ignore
        self._socket.setblocking(not nonblocking)

    def set_read_timeout(self, dur: float | None) -> None:  # type: ignore
        self._socket.settimeout(dur)

    def set_ttl(self, ttl: int) -> None:  # type: ignore
        import socket
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    def take_error(self) -> Exception | None:  # type: ignore
        try:
            err = self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            if err != 0:
                return OSError(err, os.strerror(err))
        except Exception:
            pass
        return None

    def into_inner(self) -> Any:  # type: ignore
        return self._socket

    def __enter__(self) -> UdpSocket:
        return self

    def __exit__(self, *_: Any) -> None:  # type: ignore
        pass

    def __repr__(self) -> str:
        return f"UdpSocket({self._addr})"
