"""LinkedList — a doubly-linked list."""
from __future__ import annotations
"""LinkedList — a doubly-linked list.

Provides LinkedList with push_front, push_back, pop_front, pop_back,
and drain operations.
"""

from typing import Generic, Iterable, Iterator, TypeVar

from .extra import Drain

T = TypeVar("T")


class LinkedListNode(Generic[T]):
    __slots__ = ("value", "next", "prev")

    def __init__(self, value: T) -> None:
        self.value = value
        self.next: LinkedListNode[T] | None = None
        self.prev: LinkedListNode[T] | None = None


class LinkedList(Generic[T]):
    __slots__ = ("_head", "_tail", "_len")

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._head: LinkedListNode[T] | None = None
        self._tail: LinkedListNode[T] | None = None
        self._len = 0
        if values is not None:
            for v in values:
                self.push_back(v)

    @classmethod
    def new(cls) -> LinkedList[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> LinkedList[T]:
        return cls(values)

    def push_front(self, value: T) -> None:
        node = LinkedListNode(value)
        if self._head is None:
            self._head = node
            self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._len += 1

    def push_back(self, value: T) -> None:
        node = LinkedListNode(value)
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._len += 1

    def pop_front(self) -> T | None:
        if self._head is None:
            return None
        value = self._head.value
        if self._head == self._tail:
            self._head = None
            self._tail = None
        else:
            self._head = self._head.next
            if self._head:
                self._head.prev = None
        self._len -= 1
        return value

    def pop_back(self) -> T | None:
        if self._tail is None:
            return None
        value = self._tail.value
        if self._head == self._tail:
            self._head = None
            self._tail = None
        else:
            self._tail = self._tail.prev
            if self._tail:
                self._tail.next = None
        self._len -= 1
        return value

    def front(self) -> T | None:
        return self._head.value if self._head else None

    def back(self) -> T | None:
        return self._tail.value if self._tail else None

    def len(self) -> int:
        return self._len

    def is_empty(self) -> bool:
        return self._len == 0

    def clear(self) -> None:
        self._head = None
        self._tail = None
        self._len = 0

    def contains(self, value: T) -> bool:
        node = self._head
        while node:
            if node.value == value:
                return True
            node = node.next
        return False

    def reverse(self) -> None:
        node = self._head
        while node:
            node.next, node.prev = node.prev, node.next
            node = node.prev
        self._head, self._tail = self._tail, self._head

    def iter(self) -> Iterator[T]:
        node = self._head
        while node:
            yield node.value
            node = node.next

    def iter_rev(self) -> Iterator[T]:
        node = self._tail
        while node:
            yield node.value
            node = node.prev

    def drain(self) -> Drain[T]:
        items = list(self.iter())
        self.clear()
        return Drain(items)

    def to_list(self) -> list[T]:
        return list(self.iter())

    def __len__(self) -> int:
        return self._len

    def __iter__(self) -> Iterator[T]:
        return self.iter()

    def __contains__(self, value: object) -> bool:
        return self.contains(value)  # type: ignore[arg-type]

    def __repr__(self) -> str:
        return f"LinkedList({self.to_list()})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LinkedList):
            return self.to_list() == other.to_list()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self.iter()))

    def __bool__(self) -> bool:
        return self._len > 0
