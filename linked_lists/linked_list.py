from __future__ import annotations
from typing import Iterable, Self


class Node:
    def __init__(self: Self, data: object, next: Node = None) -> None:
        self.data: object = data
        self.next: Node = next


class LinkedList:
    def __init__(self: Self, elements: Iterable = None):
        self.size: int = 0
        self.head: Node = None
        self.tail: Node = None
        if elements:
            for e in elements:
                self.add_to_tail(e)

    def __iter__(self) -> Self:
        self.iter_node = self.head
        return self

    def __next__(self) -> Node:
        if self.iter_node == None:
            raise StopIteration
        return_node = self.iter_node
        self.iter_node = self.iter_node.next
        return return_node

    def __str__(self) -> str:
        return f"LinkedList{tuple(node.data for node in self)}"

    def add(self: Self, data: object, position: int = None) -> Node:
        if position == 0:
            return self.add_to_head(data)
        if position == self.size or position == None:
            return self.add_to_tail(data)
        if position < 0 or position > self.size:
            raise IndexError("linked list index out of range")
        self.size += 1
        node = Node(data)
        tnode = self.head
        for _ in range(position - 1):
            tnode = tnode.next
        node.next = tnode.next
        tnode.next = node
        return node

    def add_to_head(self: Self, data: object) -> Node:
        self.size += 1
        node = Node(data)
        if not self.head:
            self.head = self.tail = node
        node.next = self.head
        self.head = node
        return node

    def add_to_tail(self: Self, data: object) -> Node:
        self.size += 1
        node = Node(data)
        if not self.tail:
            self.head = self.tail = node
            return node
        self.tail.next = node
        self.tail = node
        return node
