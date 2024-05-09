from __future__ import annotations
from typing import Iterable, Self


class Node:
    def __init__(self: Self, data: object, next: Node = None) -> None:
        self.data: object = data
        self.next: Node = next

    def __str__(self: Self):
        return str(f"Node({self.data})")

    def __lt__(self: Self, other: Node) -> bool:
        return self.data < other.data

    def __gt__(self: Self, other: Node) -> bool:
        return self.data > other.data

    def __eq__(self: Self, other: Node) -> bool:
        return self.data == other.data

    def __le__(self: Self, other: Node) -> bool:
        return self.data <= other.data

    def __ge__(self: Self, other: Node) -> bool:
        return self.data >= other.data

    def __ne__(self: Self, other: Node) -> bool:
        return self.data != other.data


class LinkedList:
    def __init__(self: Self, elements: Iterable = None) -> None:
        self.size: int = 0
        self.head: Node = None
        self.tail: Node = None
        if elements:
            for e in elements:
                self.append(e)

    def __len__(self: Self) -> int:
        return self.size

    def __getitem__(self: Self, key: int | slice, type: type = None) -> Self | object:
        type = LinkedList if type is None else type
        if isinstance(key, slice):
            start = 0 if key.start is None else key.start
            stop = len(self) if key.stop is None else key.stop
            step = 1 if key.step is None else key.step
            linked_list = type()
            step_count = 0
            for i, node in enumerate(self):
                if start <= i < stop:
                    if step_count % step == 0:
                        linked_list.insert(node.data)
                    step_count += 1
                elif i >= stop:
                    break
            return linked_list

        elif isinstance(key, int):
            return self.get(key)

        else:
            raise TypeError("invalid argument type")

    def __setitem__(
        self: Self, key: int | slice, value: object | Node | Iterable | LinkedList
    ) -> None:
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
            self.get(key).data = value.data if isinstance(value, Node) else value

        else:
            raise TypeError("invalid argument type")

    def __delitem__(self: Self, key: int | slice) -> None:
        if isinstance(key, slice):
            start = 0 if key.start is None else key.start
            stop = len(self) if key.stop is None else key.stop
            step = 1 if key.step is None else key.step
            if step == 1:
                self.decouple(start, stop)
            elif step > 1:
                step_count = 0
                node, prev = None, None
                for i in range(len(self)):
                    node = self.head if node is None else node.next
                    if start <= i < stop:
                        if step_count % step == 0:
                            if node == self.head:
                                self.head = node.next
                                if node == self.tail:
                                    self.tail = None
                            else:
                                prev.next = node.next
                                if node == self.tail:
                                    self.tail = prev
                            self.size -= 1
                        step_count += 1
                    elif i >= stop:
                        break
                    prev = node
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
        if self.iter_node is None:
            raise StopIteration
        node = self.iter_node
        self.iter_node = self.iter_node.next
        return node

    def __str__(self: Self) -> str:
        return f"LinkedList{tuple([node.data for node in self])}"

    def __add__(self: Self, item: LinkedList) -> Self:
        return self.copy().join(item)

    def __mul__(self: Self, value: int, type: type = None) -> Self:
        type = LinkedList if type is None else type
        linked_list = type()
        for _ in range(value):
            linked_list += self
        return linked_list

    def __lt__(self, other) -> bool:
        for node_self, node_other in zip(self, other):
            if node_self >= node_other:
                return False
        return True

    def __gt__(self, other) -> bool:
        for node_self, node_other in zip(self, other):
            if node_self <= node_other:
                return False
        return True

    def __eq__(self, other) -> bool:
        for node_self, node_other in zip(self, other):
            if node_self != node_other:
                return False
        return True

    def __le__(self, other) -> bool:
        return not self.__gt__(other)

    def __ge__(self, other) -> bool:
        return not self.__lt__(other)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def get(self: Self, index: int) -> Node:
        index += len(self) if index < 0 else 0
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
                self.tail = node
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
            return
        self.tail.next = node
        self.tail = node

    def extend(self: Self, iterable: Iterable) -> None:
        self.join(LinkedList(iterable))

    def join(self: Self, linked_list: LinkedList) -> Self:
        if self.head is None:
            self.head = linked_list.head
        else:
            self.tail.next = linked_list.head
        self.tail = linked_list.tail
        self.size += linked_list.size
        return self

    def couple(self: Self, linked_list: LinkedList, position: int) -> Self:
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
        position += len(self) if position < 0 else 0
        if position < 0 or position >= len(self):
            raise IndexError("linked list index out of range")
        self.size -= 1
        if position == 0:
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

    def decouple(self, start: int = 0, stop: int = None) -> Self:
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
            self.head = self.get(stop)
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
        for i, node in enumerate(self):
            if stop <= 0 or nindices <= 0:
                break
            if start <= 0 and node.data in data:
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

    def copy(self: Self) -> LinkedList:
        return LinkedList((data for data in self))

    def to_list(self: Self) -> list:
        return [node.data for node in self]

    def to_tuple(self: Self) -> tuple:
        return tuple(node.data for node in self)

    def to_set(self: Self) -> set:
        return set(node.data for node in self)


class CircularLinkedList(LinkedList):
    def __init__(self: Self, elements: Iterable = None):
        super().__init__(elements)

    def __getitem__(self: Self, key: int | slice) -> Self | object:
        if isinstance(key, int):
            return super().__getitem__(key % len(self), CircularLinkedList)
        return super().__getitem__(key, CircularLinkedList)

    def __setitem__(
        self: Self, key: int | slice, value: object | Iterable | LinkedList
    ) -> None:
        if isinstance(key, int):
            return super().__setitem__(key % len(self), value)
        return super().__setitem__(key, value)

    def __delitem__(self: Self, key: int | slice) -> None:
        if isinstance(key, int):
            return super().__delitem__(key % len(self))
        return super().__delitem__(key)

    def __iter__(self: Self) -> Self:
        self.iter_node = self.head
        self.i = 0
        return self

    def __next__(self: Self) -> Node:
        if self.i >= len(self):
            raise StopIteration
        self.i += 1
        data = self.iter_node.data
        self.iter_node = self.iter_node.next
        return data

    def __str__(self: Self) -> str:
        return f"CircularLinkedList{tuple([node.data for node in self])}"

    def __mul__(self: Self, value: int) -> Self:
        return super().__mul__(value, CircularLinkedList)

    def get(self: Self, index: int) -> Node:
        return super().get(index % len(self))

    def insert(self: Self, data: object, position: int = None) -> None:
        if position is None:
            return self.append(data)
        position += self.size if position < 0 else 0
        if position == len(self):
            return self.append(data)
        if position < 0 or position > len(self):
            raise IndexError(
                "cirlcular linked list index out of range, insertion does not support cyclic indexing"
            )
        self.size += 1
        node = Node(data)
        if position == 0:
            if not self.head:
                self.head = self.tail = node
                self.head.next = self.tail.next = node
            node.next = self.head
            self.head = node
            self.tail.next = self.head
        else:
            prev = self.get(position - 1)
            node.next = prev.next
            prev.next = node

    def append(self: Self, data: object) -> None:
        self.size += 1
        node = Node(data, self.head)
        if not self.tail:
            self.head = self.tail = node
            self.head.next = self.tail.next = node
            return
        self.tail.next = node
        self.tail = node

    def join(self: Self, linked_list: LinkedList) -> CircularLinkedList:
        if self.head is None:
            self.head = linked_list.head
        else:
            self.tail.next = linked_list.head
        linked_list.tail.next = self.head
        self.tail = linked_list.tail
        self.size += linked_list.size
        return self

    def couple(self: Self, linked_list: LinkedList, position: int) -> Self:
        position += len(self) if position < 0 else 0
        if position == len(self):
            return self.join(linked_list)
        if position == 0:
            linked_list.tail.next = self.head
            self.head = linked_list.head
            self.tail.next = self.head
        elif position > len(self):
            raise IndexError(
                "cirlcular linked list index out of range, insertion does not support cyclic indexing"
            )
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
        position %= len(self)
        self.size -= 1
        if position == 0:
            node = self.head
            if len(self) == 0:
                self.head = self.tail = None
            else:
                self.head = self.head.next
                self.tail.next = self.head
        else:
            prev = self.get(position - 1)
            node = prev.next
            if position == len(self):
                self.tail = prev
                prev.next = self.head
            else:
                prev.next = node.next
        return node

    def decouple(self, start: int = 0, stop: int = None) -> Self:
        if stop is None:
            stop = len(self)
        start += len(self) if start < 0 else 0
        stop += len(self) if stop < 0 else 0
        if start < 0 or stop < 0 or start >= len(self) or stop > len(self):
            raise IndexError(
                "circular list index out of range, non-inclusion stop does not support cyclic indexing"
            )
        if start > stop:
            start, stop = stop, start
        if stop - start == len(self):
            self.head = None
            self.tail = None
            self.size = 0
            return self
        if start == 0:
            self.head = self.get(stop)
        else:
            node = self.get(start - 1)
            if stop == len(self):
                self.tail = node
            else:
                node.next = self.get(stop - 1).next
        self.tail.next = self.head

        self.size -= stop - start
        return self

    def copy(self: Self) -> CircularLinkedList:
        return CircularLinkedList((data for data in self))


class DNode(Node):
    def __init__(
        self: Self, data: object, prev: DNode = None, next: DNode = None
    ) -> None:
        super().__init__(data, next)
        self.prev = prev

    def __str__(self: Self):
        return str(f"DNode({self.data})")


class DoublyLinkedList(LinkedList):
    def __init__(self: Self, elements: Iterable = None) -> None:
        self.size: int = 0
        self.head: DNode = None
        self.tail: DNode = None
        if elements:
            for e in elements:
                self.append(e)

    def __str__(self: Self) -> str:
        return f"DoublyLinkedList{tuple([node.data for node in self])}"

    def __mul__(self: Self, value: int) -> None:
        return super().__mul__(value, DoublyLinkedList)

    def insert(self: Self, data: object, position: int = None) -> None:
        if position is None:
            return self.append(data)
        position += self.size if position < 0 else 0
        if position == len(self):
            return self.append(data)
        if position < 0 or position > len(self):
            raise IndexError("linked list index out of range")
        self.size += 1
        node = DNode(data)
        if position == 0:
            if not self.head:
                self.tail = node
            else:
                self.head.prev = node
            node.next = self.head
            self.head = node
        else:
            prev = self.get(position - 1)
            node.prev, node.next = prev, prev.next
            prev.next, node.next.prev = node, node

    def append(self: Self, data: object) -> None:
        self.size += 1
        node = DNode(data, self.tail)
        if node.prev:
            node.prev.next = node
        else:
            self.head = node
        self.tail = node

    def join(self: Self, linked_list: LinkedList) -> Self:
        linked_list = (
            DoublyLinkedList(linked_list)
            if not isinstance(linked_list, DoublyLinkedList)
            else linked_list
        )
        if self.head is None:
            self.head = linked_list.head
        else:
            linked_list.head.prev = self.tail
            self.tail.next = linked_list.head
        self.tail = linked_list.tail
        self.size += linked_list.size
        return self

    def couple(self: Self, linked_list: LinkedList, position: int) -> Self:
        if position == len(self):
            return self.join(linked_list)
        if position == 0:
            self.head.prev = linked_list.tail
            linked_list.tail.next = self.head
            self.head = linked_list.head
        else:
            node = self.get(position - 1)
            node.next.prev = linked_list.tail
            linked_list.tail.next = node.next
            linked_list.head.prev = node
            node.next = linked_list.head
        self.size += linked_list.size
        return self

    def copy(self: Self) -> DoublyLinkedList:
        return DoublyLinkedList((data for data in self))
