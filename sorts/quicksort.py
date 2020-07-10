from typing import MutableSequence, Hashable
from random import shuffle


def exchange(lst, idx_a, idx_b):
    swap = lst[idx_a]
    lst[idx_a] = lst[idx_b]
    lst[idx_b] = swap
    return None


def partition(a: MutableSequence[Hashable], lo: int, hi: int) -> int:
    i = lo + 1
    j = hi
    while True:
        while a[i] < a[lo]:
            i += 1
            if i == hi:
                break
        while a[lo] < a[j]:
            j -= 1
            if j == lo:
                break
        if i >= j:
            exchange(a, lo, j)
            break
        exchange(a, i, j)
    return j


def sort(a: MutableSequence, lo: int, hi: int):
    if hi <= lo:
        return None
    j = partition(a, lo, hi)
    sort(a, lo, j - 1)
    sort(a, j + 1, hi)


def quicksort(a: MutableSequence):
    shuffle(a)
    sort(a, 0, len(a) - 1)
    return None


def quickselect(a: MutableSequence, k: int):
    shuffle(a)
    lo = 0
    hi = len(a) - 1
    while hi > lo:
        j = partition(a, lo, hi)
        if j < k:
            lo = j + 1
        elif j > k:
            hi = j - 1
        else:
            return a[k]
    return a[k]


def three_way_sort(a: MutableSequence, lo, hi):
    if hi <= lo:
        return None
    lt = lo
    gt = hi
    v = a[lo]
    i = lo
    while i <= gt:
        if a[i] < v:
            exchange(a, lt, i)
            lt += 1
            i += 1
        elif a[i] > v:
            exchange(a, i, gt)
            gt -= 1
        else:
            i += 1
    three_way_sort(a, lo, lt - 1)
    three_way_sort(a, gt + 1, hi)
    return None


def three_way_quicksort(a: MutableSequence):
    shuffle(a)
    three_way_sort(a, 0, len(a) - 1)
    return None


if __name__ == "__main__":
    a = list("QUICKSORTEXAMPLE")
    quicksort(a)
    print(a)

    b = list("QUICKSORTEXAMPLE")
    three_way_quicksort(b)
    print(b)