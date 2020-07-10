from typing import Hashable, MutableSequence
from random import randrange


def exchange(lst, idx_a, idx_b):
    swap = lst[idx_a]
    lst[idx_a] = lst[idx_b]
    lst[idx_b] = swap
    return None


def selection_sort(to_sort: MutableSequence[Hashable]):
    n = len(to_sort)
    for i in range(n):
        minimum = i
        for j in range(i + 1, n):
            if to_sort[j] < to_sort[minimum]:
                minimum = j
        exchange(to_sort, i, minimum)
    return None


def insertion_sort(to_sort: MutableSequence[Hashable]):
    for i in range(len(to_sort)):
        for j in range(i, -1, -1):
            if to_sort[j - 1] > to_sort[j]:
                exchange(to_sort, j, j - 1)
            else:
                break
    return None


def h_sort(to_sort: MutableSequence[Hashable], h):
    for i in range(h, len(to_sort)):
        for j in range(i, h - 1, -1 * h):
            if to_sort[j - h] > to_sort[j]:
                exchange(to_sort, j, j - h)
            else:
                break
    return None


def shell_sort(to_sort: MutableSequence[Hashable]):
    i = 2
    h = 1
    hs = [h]
    while h < len(to_sort) // 3:
        h = (3 ** i - 1) // 2
        hs.append(h)
        i += 1
    for h in hs[::-1]:
        h_sort(to_sort, h)
    return None


def knuth_shuffle(to_shuffle: MutableSequence[Hashable]):
    for i in range(1, len(to_shuffle)):
        j = randrange(0, i + 1)
        exchange(to_shuffle, i, j)
    return None
