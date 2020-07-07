"""
Dynamic connectivity algorithms:

Given a set of n objects,
union command: connect two objects
find query: is there a path connecting the two objects?

These algorithms are more efficient than pathfinding algorithms because they
do not need to preserve the path,
only the fact that there is one. 'is connected to' is an equivalence relation;
these algorithms exploit that fact
"""
                

class QuickFindUF():
    """The text's first approach:
    Eager
    initialize: O(n)
    union: O(n) <-- this is still a problem for n unions
    find: O(1)
    """    
    def __init__(self, n: int):
        self.components = list(range(0, n))
        
    def find(self, n1, n2):
        return self.components[n1] == self.components[n2]
    
    def union(self, n1, n2):
        self.components = [self.components[n2] 
                           if self.components[n1] == n 
                           else n 
                           for n in self.components]


class QuickUnionUF():
    """Lazy approach
    Interpretation: id[i] is parent of i
    Root of i is id[id[...id[i]...]] <-- keep going until it doesn't change
            algorithm ensures no cycles
    initialize: O(n)
    union: O(n) <-- includes cost of finding roots
    find: O(n)
    """
    def __init__(self, n: int):
        self.components = list(range(0, n))
    
    def find(self, n1, n2):
        return self._root(n1) == self._root(n2)
    
    def union(self, n1, n2):
        r1 = self._root(n1)
        self.components[r1] = self._root(n2)
     
    def _root(self, n):
        while n != self.components[n]:
            n = self.components[n]
        return n


"""
For quick-find, union is too expensive (n array accesses)
Trees are flat, but too expensive to keep them flat

For quick-union, trees can get tall
Find is too expensive (could be n array accesses)
"""


class WeightedQuickUnionUF(QuickUnionUF):
    """Avoid tall trees by keeping track of the size of each tree
    (number of objects)
    Balance by linking root of smaller tree to root of larger tree
    initialize: O(n)
    find: O(log_2(n)) <- tree stays balanced, depth is at most log_2(n)
    union: O(log_2(n)) <- constant time, given roots
    """
    def __init__(self, n: int):
        super().__init__(n)
        self.sz = [1 for n in self.components]
        
    def find(self, n1, n2):
        return self._root(n1) == self._root(n2)
        
    def union(self, n1, n2):
        r1 = self._root(n1)
        r2 = self._root(n2)
        if r1 == r2:
            pass
        elif self.sz[r1] < self.sz[r2]:
            self.components[r1] = r2
            self.sz[r2] += self.sz[r1]
        else:
            self.components[r2] = r1
            self.sz[r1] += self.sz[r2]

        
class WeightedQuickUnionPathCompressionUF(WeightedQuickUnionUF):
    """
    After finding the root, compress the nodes on the path
    to keep the tree as flat as possible.
    """
    def _root(self, n1):
        def parent(n):
            return self.components[n]
        nodes = [n1]
        while n1 != parent(n1):
            n1 = parent(n1)
            nodes.append(n1)
        root = n1
        for n in nodes:
            self.components[n] = root
        return root