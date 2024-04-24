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

    def __setitem__(
        self: Self, key: int | slice, value: object | Iterable | LinkedList
    ):
        if isinstance(key, slice):
            if not isinstance(value, Iterable):
                raise TypeError(
                    "invalid argument type, slice assignment only accepts iterables"
                )
            start = 0 if key.start is None else key.start
            stop = len(self) if key.stop is None else key.stop
            step = 1 if key.step is None else key.step
            if step == 1:
                del self[start:stop]
                self.couple(
                    value if isinstance(value, LinkedList) else LinkedList(value), start
                )
            elif step > 1:
                slice_size = (stop - start) // step + 1 * ((stop - start) % step != 0)
                if slice_size != len(value):
                    raise ValueError(
                        f"attempt to assign sequence of size {len(value)} to extended slice of size {slice_size}"
                    )
                step_count = 0
                value_count = 0
                for i in range(len(self)):
                    if start <= i < stop:
                        if step_count % step == 0:
                            self[i] = value[value_count]
                            value_count += 1
                        step_count += 1
                    elif i >= stop:
                        break
            else:
                raise ValueError("negative steps are currently not supported")

        elif isinstance(key, int):
            self.get(key).data = value

        else:
            raise TypeError("invalid argument type")

    # TODO optimize
    def __delitem__(self: Self, key: int | slice) -> None:
        if isinstance(key, slice):
            start = 0 if key.start is None else key.start
            stop = len(self) if key.stop is None else key.stop
            step = 1 if key.step is None else key.step
            if step == 1:
                self.decouple(start, stop)
            elif step > 1:
                step_count = 0
                deletion_count = 0
                for i in range(len(self)):
                    if start <= i < stop:
                        if step_count % step == 0:
                            self.pop(i - deletion_count)
                            deletion_count += 1
                        step_count += 1
                    elif i >= stop:
                        break
            elif step < 0:
                raise ValueError("negative steps are currently not supported")

        elif isinstance(key, int):
            self.pop(key)

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

    def __mul__(self: Self, value: int) -> LinkedList:
        linked_list = LinkedList()
        for _ in range(value):
            linked_list += self
        return linked_list

    def get(self: Self, index: int):
        if 0 <= index < len(self):
            node = self.head
            for _ in range(index):
                node = node.next
            return node
        raise IndexError("linked list index out of range")

    def insert(self: Self, data: object, position: int = None) -> None:
        if position is None:
            return self.append(data)
        position += self.size if position < 0 else 0
        if position == len(self):
            return self.append(data)
        if position < 0 or position > len(self):
            raise IndexError("linked list index out of range")
        self.size += 1
        node = Node(data)
        if position == 0:
            if not self.head:
                self.head = self.tail = node
            node.next = self.head
            self.head = node
        else:
            prev = self.get(position - 1)
            node.next = prev.next
            prev.next = node

    def append(self: Self, data: object) -> None:
        self.size += 1
        node = Node(data)
        if not self.tail:
            self.head = self.tail = node
            return node
        self.tail.next = node
        self.tail = node

    def extend(self: Self, iterable: Iterable) -> None:
        self.join(LinkedList(iterable))

    def join(self: Self, linked_list: LinkedList) -> LinkedList:
        if self.head is None:
            self.head = linked_list.head
        else:
            self.tail.next = linked_list.head
        self.tail = linked_list.tail
        self.size += linked_list.size
        return self

    def couple(self: Self, linked_list: LinkedList, position: int) -> LinkedList:
        if position == len(self):
            return self.join(linked_list)
        if position == 0:
            linked_list.tail.next = self.head
            self.head = linked_list.head
        else:
            node = self.get(position - 1)
            linked_list.tail.next = node.next
            node.next = linked_list.head
        self.size += linked_list.size
        return self

    def pop(self: Self, position: int = None) -> Node:
        if position is None:
            if len(self) <= 0:
                raise TypeError("linked list is empty")
            position = len(self) - 1
        position += self.size if position < 0 else 0
        if position < 0 or position >= len(self):
            raise IndexError("linked list index out of range")
        self.size -= 1
        if position == 0:
            self.size -= 1
            node = self.head
            self.head = self.head.next
            if len(self) == 0:
                self.tail = None
        else:
            prev = self.get(position - 1)
            node = prev.next
            if position == len(self):
                self.tail = prev
                prev.next = None
            else:
                prev.next = node.next
        return node

    def decouple(self, start: int = 0, stop: int = None) -> LinkedList:
        if stop is None:
            stop = len(self)
        start += len(self) if start < 0 else 0
        stop += len(self) if stop < 0 else 0
        if start < 0 or stop < 0 or start >= len(self) or stop > len(self):
            raise IndexError("index out of range")
        if start > stop:
            start, stop = stop, start
        if stop - start == len(self):
            self.head = None
            self.tail = None
            self.size = 0
            return self
        if start == 0:
            self.head = self.get(stop - 1).next
            if self.head.next is None:
                self.tail = self.head
        else:
            node = self.get(start - 1)
            node.next = self.get(stop - 1).next
            if node.next is None:
                self.tail = node

        self.size -= stop - start
        return self

    def index(
        self: Self,
        data: object | tuple,
        start=0,
        stop=None,
        step=1,
        skip=0,
        nindices=None,
        return_all=False,
    ):
        if step <= 0:
            raise ValueError("negative steps are currently not supported")
        start += len(self) if start < 0 else 0
        start = 0 if start < 0 else start
        if nindices is None:
            nindices = len(self) if return_all else 1
        if stop is None:
            stop = len(self)
        if len(self) <= 0 or nindices <= 0:
            return None
        if not isinstance(data, tuple):
            data = [data]
        indices = []
        step_count = 0
        for i, node_data in enumerate(self):
            if stop <= 0 or nindices <= 0:
                break
            if start <= 0 and node_data in data:
                if skip <= 0:
                    if step_count % step == 0:
                        indices.append(i)
                        nindices -= 1
                    step_count += 1
                else:
                    skip -= 1
            start -= 1
            stop -= 1
        if len(indices) <= 0:
            return None
        return indices if nindices > 0 or len(indices) > 1 else indices[0]

    def copy(self: Self):
        return LinkedList((data for data in self))
