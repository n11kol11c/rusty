"""TcpStream and TcpListener — TCP client and server."""
from __future__ import annotations

"""TCP networking — streams and listeners.

Provides TcpStream for client connections and TcpListener for
server sockets with accept, incoming, and stream operations.
"""

from typing import Any

from .address import SocketAddr, Shutdown


class TcpStream:
    __slots__ = ("_stream", "_addr")

    def __init__(self, stream: Any, addr: SocketAddr | None = None) -> None:
        self._stream = stream
        self._addr = addr

    @classmethod
    def connect(cls, addr: SocketAddr) -> TcpStream:
        import socket
        sock = socket.socket(
            socket.AF_INET if addr.is_ipv4() else socket.AF_INET6,
            socket.SOCK_STREAM,
        )
        sock.connect(addr.to_socket_addr())
        sock.setblocking(True)
        return TcpStream(sock, addr)

    @classmethod
    def connect_timeout(cls, addr: SocketAddr, timeout: float) -> TcpStream:
        import socket
        sock = socket.socket(
            socket.AF_INET if addr.is_ipv4() else socket.AF_INET6,
            socket.SOCK_STREAM,
        )
        sock.settimeout(timeout)
        sock.connect(addr.to_socket_addr())
        sock.setblocking(True)
        return TcpStream(sock, addr)

    @classmethod
    def from_stream(cls, stream: Any, addr: SocketAddr | None = None) -> TcpStream:
        return TcpStream(stream, addr)

    def peer_addr(self) -> SocketAddr | None:  # type: ignore
        if self._addr:
            return self._addr
        if self._stream:
            try:
                addr = self._stream.getpeername()
                return SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
            except Exception:
                pass
        return None

    def local_addr(self) -> SocketAddr | None:  # type: ignore
        if self._stream:
            try:
                addr = self._stream.getsockname()
                return SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
            except Exception:
                pass
        return None

    def shutdown(self, how: Shutdown) -> None:  # type: ignore
        import socket
        if not self._stream:
            return
        if how.kind() == Shutdown.READ:
            self._stream.shutdown(socket.SHUT_RD)
        elif how.kind() == Shutdown.WRITE:
            self._stream.shutdown(socket.SHUT_WR)
        else:
            self._stream.shutdown(socket.SHUT_RDWR)

    def set_nodelay(self, nodelay: bool) -> None:  # type: ignore
        if self._stream:
            self._stream.setsockopt(
                __import__('socket').IPPROTO_TCP,
                __import__('socket').TCP_NODELAY,
                1 if nodelay else 0,
            )

    def set_nonblocking(self, nonblocking: bool) -> None:  # type: ignore
        if self._stream:
            self._stream.setblocking(not nonblocking)

    def set_read_timeout(self, dur: float | None) -> None:  # type: ignore
        if self._stream:
            self._stream.settimeout(dur)

    def set_write_timeout(self, dur: float | None) -> None:  # type: ignore
        if self._stream:
            self._stream.settimeout(dur)

    def read(self, buf: bytearray) -> int:  # type: ignore
        return self._stream.recv_into(buf)  # type: ignore

    def write(self, data: bytes | bytearray) -> int:  # type: ignore
        return self._stream.send(data)  # type: ignore

    def write_all(self, data: bytes | bytearray) -> None:  # type: ignore
        total = 0
        while total < len(data):
            n = self._stream.send(data[total:])  # type: ignore
            total += n

    def try_clone(self) -> TcpStream:  # type: ignore
        import socket
        new_sock = socket.dup(self._stream)  # type: ignore
        return TcpStream(new_sock, self._addr)

    def into_inner(self) -> Any:  # type: ignore
        return self._stream

    def as_raw_fd(self) -> Any:  # type: ignore
        return self._stream

    def __enter__(self) -> TcpStream:
        return self

    def __exit__(self, *_: Any) -> None:
        try:
            self._stream.close()
        except Exception:
            pass

    def __repr__(self) -> str:
        return f"TcpStream({self._addr})"


class TcpListener:
    __slots__ = ("_listener", "_addr")

    def __init__(self, listener: Any, addr: SocketAddr | None = None) -> None:
        self._listener = listener
        self._addr = addr

    @classmethod
    def bind(cls, addr: SocketAddr) -> TcpListener:
        import socket
        sock = socket.socket(
            socket.AF_INET if addr.is_ipv4() else socket.AF_INET6,
            socket.SOCK_STREAM,
        )
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addr.to_socket_addr())
        sock.listen(128)
        return TcpListener(sock, addr)

    @classmethod
    def from_std(cls, listener: Any, addr: SocketAddr | None = None) -> TcpListener:
        return TcpListener(listener, addr)

    def local_addr(self) -> SocketAddr | None:  # type: ignore
        if self._listener:
            try:
                addr = self._listener.getsockname()
                return SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
            except Exception:
                pass
        return None

    def accept(self) -> tuple[TcpStream, SocketAddr]:  # type: ignore
        conn, addr = self._listener.accept()  # type: ignore
        sock_addr = SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
        return TcpStream(conn, sock_addr), sock_addr

    def accept_timeout(self, timeout: float) -> tuple[TcpStream, SocketAddr] | None:  # type: ignore
        import socket
        self._listener.settimeout(timeout)  # type: ignore
        try:
            return self.accept()
        except socket.timeout:
            return None
        finally:
            self._listener.setblocking(True)  # type: ignore

    def incoming(self) -> Incoming:  # type: ignore
        return Incoming(self)

    def set_nonblocking(self, nonblocking: bool) -> None:  # type: ignore
        if self._listener:
            self._listener.setblocking(not nonblocking)

    def into_inner(self) -> Any:  # type: ignore
        return self._listener

    def __enter__(self) -> TcpListener:
        return self

    def __exit__(self, *_: Any) -> None:  # type: ignore
        pass

    def __repr__(self) -> str:
        return f"TcpListener({self._addr})"


class Incoming:
    __slots__ = ("_listener", "_done")

    def __init__(self, listener: TcpListener) -> None:
        self._listener = listener
        self._done = False

    def __iter__(self) -> Incoming:
        return self

    def __next__(self) -> TcpStream:
        if self._done:
            raise StopIteration
        try:
            conn, _ = self._listener.accept()
            return conn
        except Exception:
            self._done = True
            raise StopIteration
