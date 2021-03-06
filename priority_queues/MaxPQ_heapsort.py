from typing import MutableSequence, Hashable


class MaxPQ():
    def __init__(self):
        self.a = [None]
        self.n = 0
        self.size = 0

    def insert(self, item):
        if self.n == self.size:
            self._resize(max(1, self.n) * 2)
        self.n += 1
        self.a[self.n] = item
        self._swim(self.n)
        return None

    def del_max(self):
        max_val = self.max()
        self._exch(1, self.n)
        self.a[self.n] = None  # prevent loitering
        self.n -= 1
        if (self.n * 4) == self.size:
            self._resize(self.n * 2)
        self._sink(1)
        return max_val

    def max(self):
        if self.n > 0:
            return self.a[1]
        else:
            raise IndexError("queue is empty")

    def is_empty(self):
        return self.n == 0

    def _swim(self, k):
        while k > 1 and self._less(k // 2, k):
            self._exch(k, k // 2)
            k = k // 2
        return None

    def _sink(self, k):
        while 2 * k <= self.n:
            j = 2 * k
            if j < self.n and self._less(j, j + 1):
                j += 1
            if self._less(j, k):
                break
            self._exch(k, j)
            k = j
        return None

    def _less(self, l_idx, r_idx):
        if l_idx is None:
            return False
        elif r_idx is None:
            return True
        else:
            return self.a[l_idx] < self.a[r_idx]

    def _exch(self, a_idx, b_idx):
        swap = self.a[a_idx]
        self.a[a_idx] = self.a[b_idx]
        self.a[b_idx] = swap
        return None

    def _resize(self, capacity):
        copy = [None] * (1 + capacity)
        for i in range(1, self.n + 1):
            copy[i] = self.a[i]
        self.a = copy
        self.size = capacity
        return None

    @staticmethod
    def heapsort(lst: MutableSequence[Hashable]) -> MutableSequence[Hashable]:
        #  build heap using bottom-up method
        #  to save space, perform in place
        #  (would need to write separate class for this)
        a = MaxPQ()
        a.a.extend(lst)
        a.n = len(lst)
        for k in range(a.n // 2, 0, -1):
            a._sink(k)
        #  sortdown: remove max one at a time, leaving in array
        for i in range(a.n, 1, -1):
            a._exch(1, i)
            a.n -= 1
            a._sink(1)
        return a.a[1:(len(lst) + 1)]
