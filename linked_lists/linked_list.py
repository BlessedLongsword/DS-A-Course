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
                self.insert_tail(e)

    def __len__(self: Self) -> int:
        return self.size

    def __getitem__(self: Self, key: int | slice) -> LinkedList | object:
        if isinstance(key, slice):
            start = 0 if key.start is None else key.start
            stop = len(self) if key.stop is None else key.stop
            step = 1 if key.step is None else key.step
            linked_list = LinkedList()
            step_count = 0
            for i, data in enumerate(self):
                if start <= i < stop:
                    if step_count % step == 0:
                        linked_list.insert(data)
                    step_count += 1
                elif i >= stop:
                    break
            return linked_list

        elif isinstance(key, int):
            if key < 0:
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError("index out of range")
            for i, data in enumerate(self):
                if i == key:
                    return data

        else:
            raise TypeError("invalid argument type")

    def __iter__(self: Self) -> Self:
        self.iter_node = self.head
        return self

    def __next__(self: Self) -> Node:
        if self.iter_node == None:
            raise StopIteration
        data = self.iter_node.data
        self.iter_node = self.iter_node.next
        return data

    def __str__(self: Self) -> str:
        return f"LinkedList{tuple([data for data in self])}"

    def __add__(self: Self, item: LinkedList) -> LinkedList:
        return self.copy().join(item)

    # TODO: refactor
    def insert(self: Self, data: object, position: int = None) -> Node:
        if position == 0:
            return self.insert_head(data)
        if position == len(self) or position == None:
            return self.insert_tail(data)
        if position < 0 or position > len(self):
            raise IndexError("linked list index out of range")
        self.size += 1
        node = Node(data)
        tnode = self.head
        for _ in range(position - 1):
            tnode = tnode.next
        node.next = tnode.next
        tnode.next = node
        return node

    def insert_head(self: Self, data: object) -> Node:
        self.size += 1
        node = Node(data)
        if not self.head:
            self.head = self.tail = node
        node.next = self.head
        self.head = node
        return node

    def insert_tail(self: Self, data: object) -> Node:
        self.size += 1
        node = Node(data)
        if not self.tail:
            self.head = self.tail = node
            return node
        self.tail.next = node
        self.tail = node
        return node

    def append(self: Self, data: object) -> None:
        self.insert_tail(self, data)

    def extend(self: Self, iterable: Iterable) -> None:
        for element in iterable:
            self.insert_tail(element)

    def join(self: Self, linked_list: LinkedList) -> LinkedList:
        self.tail.next = linked_list.head
        self.tail = linked_list.tail
        return self

    # TODO: refactor
    def pop(self: Self, position: int = None) -> Node:
        if position is None:
            if len(self) <= 0:
                raise TypeError("linked list is empty")
            position = len(self) - 1
        if position == 0:
            return self.pop_head()
        if position < 0 or position >= len(self):
            raise IndexError("linked list index out of range")
        self.size -= 1
        tnode = self.head
        for _ in range(position - 1):
            tnode = tnode.next
        node = tnode.next
        if position == len(self):
            self.tail = tnode
            tnode.next = None
        else:
            tnode.next = tnode.next.next
        return node

    def pop_head(self: Self) -> Node:
        self.size -= 1
        node = self.head
        self.head = self.head.next
        if len(self) == 0:
            self.tail = None
        return node

    def pop_tail(self: Self) -> Node:
        return self.pop(len(self) - 1)

    # TODO: Refactor + add step
    def index(self: Self, data: object, start=0, stop=None, skip=0, nindices=None):
        if nindices is None:
            nindices = 1
        if stop is None:
            stop = len(self)
        if len(self) <= 0 or nindices <= 0:
            return None
        indices = []
        tnode = self.head
        i = 0
        while tnode:
            if stop <= 0 or nindices <= 0:
                break
            if start <= 0 and tnode.data == data:
                if skip <= 0:
                    indices.append(i)
                    nindices -= 1
                else:
                    skip -= 1
            i += 1
            tnode = tnode.next
            start -= 1
            stop -= 1
        if len(indices) <= 0:
            return None
        return indices if nindices > 0 or len(indices) > 1 else indices[0]

    def copy(self):
        return LinkedList((data for data in self))
