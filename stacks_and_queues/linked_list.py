from numpy import empty


""" Two implementations of a stack interface:
The first uses a linked list
the second uses a resizable array

The linked-list implementation uses more space and time
to deal with the links and is constant time in the worst case

The array implementation has less memory overhead and is
*amortized* constant time (at least in principle; we have
to import numpy arrays to get an array-like data structure)
"""


class LinkedStack():
    """
    In the real world, we would use collections.deque and
    call it a day.

    But this is a from-scratch implementation, for educational purposes.
    This should have way more memory overhead than the built-in  implementation
    but it should have similar time performance; every operation
    takes constant time in the worst case.
    """
    def __init__(self):
        self.first = None

    def is_empty(self):
        return self.first is None
    
    def push(self, item):
        self.first = _Node(item, self.first)
        return None
        
    def pop(self):
        item = self.first.item
        self.first = self.first.next
        return item
    
    def __iter__(self):
        node = self.first
        while node is not None:
            yield node.item
            node = node.next
    
    def __repr__(self):
        first = self.first
        nodes = []
        while first is not None:
            nodes.append(repr(first.item))
            first = first.next
        nodes.append("None")
        return " -> ".join(nodes)


class _Node():
    def __init__(self, item, next):
        self.item = item
        self.next = next

    def __repr__(self):
        return self.item


class ArrayStack():
    """Python's lists
    are already resizable arrays;
    numpy arrays provide fixed-size arrays for us to
    work with
    """
    def __init__(self):
        self.stack = empty(1, dtype=object)
        self.capacity = 1  # actual length of array
        self.n = 0  # actual #; index is self.n - 1
    
    def is_empty(self):
        return self.n == 0
    
    def push(self, item):
        if self.n == self.capacity:
            self._resize(2 * self.capacity)
        self.n += 1
        self.stack[self.n - 1] = item
        return None
        
    def pop(self):
        item = self.stack[self.n - 1]
        self.stack[self.n - 1] = None
        self.n -= 1
        if self.n * 4 == self.capacity:
            self._resize(self.n * 2)
        return item
    
    def __iter__(self):
        n = self.n
        while n > 0:
            yield self.stack[n - 1]
            n -= 1
                    
    def _resize(self, capacity: int):
        new_stack = empty(capacity, dtype=object)
        for i in range(self.n):
            new_stack[i] = self.stack[i]
        self.stack = new_stack
        self.capacity = capacity
        return None


class LinkedQueue():
    """The same idea as the linked stack above,
    but for a queue
    """
    def __init__(self):
        self.first = None
        self.last = None

    def __repr__(self):
        first = self.first
        nodes = ['None']
        while first is not None:
            nodes.append(repr(first.item))
            first = first.next
        return " <- ".join(nodes)

    def is_empty(self):
        return self.first is None
        pass

    def enqueue(self, item):
        oldlast = self.last
        self.last = _Node(item, None)
        if self.is_empty():  # special case for empty queue
            self.first = self.last
        else:
            oldlast.next = self.last
    
    def dequeue(self):
        """Note: identical to linked stack pop"""
        item = self.first.item
        self.first = self.first.next
        if self.is_empty():  # special case for empty queue
            self.last = None
        return item