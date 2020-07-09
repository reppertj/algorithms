"""
Write a client program permutation.py that takes an integer k
as a command-line argument; reads a sequence of strings from
standard input, and prints exactly k of them, uniformly at
random. Print each item from the sequence at most once.
"""

import sys

from deque import RandomizedQueue


if __name__ == "__main__":
    queue = RandomizedQueue()
    for word in sys.stdin.read().split():
        queue.enqueue(word)
    for i in range(int(sys.argv[1])):
        print(queue.dequeue())
