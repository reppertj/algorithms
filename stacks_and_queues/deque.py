from numpy import empty
from random import randrange

""" Create a deque supporting each deque
operation in constant worse-case time """


class MyDeque():
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0
    
    def is_empty(self):
        return self.first is None
    
    def add_first(self, item):
        if item is None:
            raise ValueError("cannot add None to deque")
        if self.is_empty():
            self.first = _Node(item, None, None)
            self.last = self.first
        else:
            new_first = _Node(item, self.first, None)
            self.first.prev = new_first
            self.first = new_first
        self.size += 1
        return None
    
    def add_last(self, item):
        if item is None:
            raise ValueError("cannot add None to deque")
        if self.is_empty():
            self.last = _Node(item, None, None)
            self.first = self.last
        else:
            new_last = _Node(item, None, self.last)
            self.last.next = new_last
            self.last = new_last
        self.size += 1
        return None

    def remove_first(self):
        if self.is_empty():
            raise IndexError("can't remove from empty deque")
        if self.first.next is None:
            item = self.first.item
            self.first = None
            self.last = None
        else:
            item = self.first.item
            self.first = self.first.next
        self.size -= 1
        return item
    
    def remove_last(self):
        if self.is_empty():
            raise IndexError("can't remove from empty deque")
        if self.last.prev is None:
            item = self.last.item
            self.last = None
            self.first = None
        else:
            item = self.last.item
            self.last = self.last.prev
        self.size -= 1
        return item

    def __iter__(self):
        node = self.first
        while node is not None:
            yield node.item
            node = node.next


class _Node():
    def __init__(self, item, nextnode, prevnode):
        self.item = item
        self.next = nextnode
        self.prev = prevnode
    

class RandomizedQueue():
    def __init__(self):
        self.queue = empty(1, dtype=object)
        self.capacity = 1  # actual length of array
        self.size = 0  # actual size; idx is self.size - 1
    
    def is_empty(self):
        return self.size == 0
    
    def enqueue(self, item):
        if item is None:
            raise ValueError("can't add None to queue")
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.size += 1
        self.queue[self.size - 1] = item
        return None
    
    def dequeue(self):
        if self.size == 0:
            raise IndexError("can't remove from empty queue")
        idx = randrange(0, self.size)
        item = self.queue[idx]
        self.queue[idx] = self.queue[self.size - 1]
        self.queue[self.size - 1] = None
        self.size -= 1
        if self.size * 4 == self.capacity:
            self._resize(self.size * 2)
        return item
    
    def __iter__(self):
        rand_items = empty(self.size, dtype=object)
        for i in range(self.size):
            rand_idx = randrange(i, self.size)
            rand_items[i] = self.queue[rand_idx]
            self.queue[rand_idx] = self.queue[i]
        for i in range(self.size):
            yield rand_items[i]

    def _resize(self, new_capacity):
        new_queue = empty(new_capacity, dtype=object)
        for i in range(self.size):
            new_queue[i] = self.queue[i]
        self.queue = new_queue
        self.capacity = new_capacity
