import random
from warnings import warn
from math import sqrt
from scipy.stats import t

import union_find

"""
Exercise: estimate the percolation threshold p* for large square lattices
(p* is known to be about 0.592746) using a Monte-Carlo simulation

Performance requirements:
Constructor must take O(n^2)
Other methods must take constant time
plus constant number of calls to union and find, which themselves must take O(log(n))
"""


class Percolation():
    def __init__(self, n, uf_class):
        """
        A cell is closed if it is 0; open if it is 1
        Top is indexed at n ** 2; bottom is indexed at n ** 2 + 1
        Top and bottom begin open and isolated.
        The matrix percolates just in case top and bottom are connected
        Keep track of count of open sites to maintain constant time
        """
        self.n = n
        self.matrix = [0 for i in range(0, self.n ** 2)] + [1, 1]
        self.no_of_open_sites = 0
        self.uf = uf_class(self.n ** 2 + 2)
        self.top = n ** 2
        self.bottom = self.top + 1

    def __str__(self):
        output = ""
        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i * self.n + j] == 1:
                    output += " "
                else:
                    output += "#"
            output += "\n"
        return output

    def is_open(self, idx):
        return self.matrix[idx] == 1

    def open(self, idx):
        if not self.is_open(idx):
            self.matrix[idx] = 1  # mark as open
            self.no_of_open_sites += 1
            for c in self._neighbors(idx):
                if self.is_open(c):  # connect to open neighbors
                    self.uf.union(idx, c)
        return None
    
    def is_full(self, idx):
        return self.uf.find(idx, self.top)
    
    def percolates(self):
        return self.uf.find(self.top, self.bottom)

    def _neighbors(self, idx):
        neighbors = []
        # above
        if idx < self.n:
            neighbors.append(self.top)
        else:
            neighbors.append(idx - self.n)
        # below
        if (self.n * (self.n - 1)) <= idx:
            neighbors.append(self.bottom)
        else:
            neighbors.append(idx + self.n)
        # left
        if idx % self.n != 0:
            neighbors.append(idx - 1)
        # right
        if idx % self.n != (self.n - 1):
            neighbors.append(idx + 1)
        return neighbors


class PercolationStats():
    """Perform independent trials on an n-by-n grid
    """
    def __init__(self, n, trials, uf_class=union_find.WeightedQuickUnionUF):
        if trials < 2:
            raise ValueError("trials must be > 1")
        elif trials < 30:
            warn("Should run at least 30 trials")
        thresholds = []
        for i in range(0, trials):
            thresholds.append(self.percolation_threshold(n, uf_class))
        self.df = trials - 1
        self.mean = sum(thresholds) / trials
        self.stddev = sum([(t - self.mean) ** 2 for t in thresholds]) / self.df
        self.stderr = self.stddev / sqrt(trials)
        CI_95 = 0.025
        self.confidenceLo = self.mean + t.ppf(CI_95, self.df) * (self.stderr)
        self.confidenceHi = self.mean - t.ppf(CI_95, self.df) * (self.stderr)
        self.stats = (f'For {trials} trials on a {n} by {n} grid:\n'
                      f'mean = {self.mean}\n'
                      f'std dev. = {self.stddev}\n'
                      f'95% confidence: [{self.confidenceLo}, {self.confidenceHi}]')

    @staticmethod
    def percolation_threshold(n, uf_class):
        choices = list(range(n ** 2))
        random.shuffle(choices)
        percolation = Percolation(n, uf_class)
        open_sites = 0
        while not percolation.percolates():
            percolation.open(choices.pop())
            open_sites += 1
        return open_sites / (n ** 2)