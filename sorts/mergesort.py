from typing import Hashable, MutableSequence


def is_sorted(a, lo, hi):
    for i in range(lo, hi):
        if a[i] > a[i + 1]:
            return False
    return True


def merge(a: MutableSequence[Hashable], aux, lo: int, mid: int, hi: int):
    # assert is_sorted(a, lo, mid)
    # assert is_sorted(a, mid + 1, hi)
    aux[lo:(hi + 1)] = a[lo:(hi + 1)]
    i = lo
    j = mid + 1
    for k in range(lo, hi + 1):
        if i > mid:
            a[k] = aux[j]
            j += 1
        elif j > hi:
            a[k] = aux[i]
            i += 1
        elif aux[i] < aux[j]:
            a[k] = aux[i]
            i += 1
        else:
            a[k] = aux[j]
            j += 1
    # assert is_sorted(a, lo, hi)
    return None


def sort(a: MutableSequence[Hashable], aux, lo, hi):
    if lo >= hi:
        return None
    mid = lo + (hi - lo) // 2
    sort(a, aux, lo, mid)
    sort(a, aux, mid + 1, hi)
    merge(a, aux, lo, mid, hi)
    return None


def mergesort(a: MutableSequence[Hashable]):
    aux = [None] * (len(a))
    sort(a, aux, 0, len(a) - 1)
    return None


def bottom_up_mergesort(a: MutableSequence[Hashable]):
    aux = [None] * len(a)
    sz = 1
    while sz < len(a):
        lo = 0
        while lo < (len(a) - sz):
            merge(a, aux, lo, lo + sz - 1, min(lo + sz + sz - 1, len(a) - 1))
            lo += (sz + sz)
        sz += sz
    return None
