import time
import random
import matplotlib.pyplot as plt
import numpy as np


import union_find
import percolation_monte_carlo

def monte_carlo_timer(qfalg, max_n, trials):
    times = []
    for n in range(2, max_n + 1):
        start = time.time()
        percolation_monte_carlo.PercolationStats(n, trials, qfalg)
        end = time.time()
        runtime = end - start
        times.append(runtime)
    return times

qfalgs_all = [
          union_find.QuickFindUF,
          union_find.QuickUnionUF,
          union_find.WeightedQuickUnionUF,
          union_find.WeightedQuickUnionPathCompressionUF,
          ]

qfalgs_qu = [
          union_find.QuickUnionUF,
          union_find.WeightedQuickUnionUF,
          union_find.WeightedQuickUnionPathCompressionUF, 
          ]

def union_find_timer_constant_operations(qfalg, max_n, max_operations):
    times = []
    for n in range(2, max_n + 1):
        start = time.time()
        uf = qfalg(n)
        for i in range(2, max_n + 1):
            u1, u2 = random.sample(range(n), 2)
            f1, f2 = random.sample(range(n), 2)
            uf.union(u1, u2)
            uf.find(u1, u2)
        end = time.time()
        runtime = end - start
        times.append(runtime)
    return times
            

def plot_times(qfalgs, timer, max_n, inner_n):
    plt.figure(figsize=(6, 6))
    idx = 1
    for alg in qfalgs:
        plt.plot(timer(alg, max_n, inner_n), label=str(alg))
        plt.ylabel('Time')
        plt.xlabel('Size')
        idx += 1
    plt.tight_layout()
    plt.legend()
    plt.show()

 
"""
What did we learn here?

Big O time isn't everything. You can often avoid the worst-case scenario by exploiting 
the quirks of an algorithm that is "worse" on paper. For the Monte Carlo simulations, 
we keep the "virtual bottom" and "virtual top as their own roots until the very end,
we keep the find calls at constant time despite the time complexity of the find algorithm.

So the time savings from balancing the tree through WeightedQuickUnion and 
WeightedQuickUnionPathCompression aren't needed, and the cost of actually doing 
the balancing and compressing makes them slightly more expensive for this application. 

But we could only do this because we knew the implementation and exploited the chirality of
the QuickUnion algorithm to avoid the worst-case scenario where find takes time O(n). Had we
reversed the order and started rooting inside the matrix, we would have lost these
savings.
"""