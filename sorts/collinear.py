from typing import List
from functools import total_ordering
from math import inf
import matplotlib.pyplot as plt

from mergesort import mergesort

"""
Exercise:
Given a set of n distinct points in the plane,
find every (maximal) line segment that connects a subset of 4 or more of the points.
"""


@total_ordering
class Point2D():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return ((self.x, self.y)) == ((other.x, other.y))

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        else:
            return self.y < other.y
 
    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))

    def slope_to(self, other):
        if self.x == other.x:
            return inf
        elif self == other:
            return -inf
        else:
            return (other.y - self.y) / (other.x - self.x)
 
    def draw(self):
        plt.plot([self.x], [self.y], 'o')
        return None


@total_ordering
class Ordered_Slopes():
    def __init__(self, central: Point2D, secondary: Point2D):
        self.central = central
        self.secondary = secondary
        
    def __hash__(self):
        return hash((self.central, self.secondary))
        
    def __eq__(self, other):
        return self.central.slope_to(self.secondary) == other.central.slope_to(other.secondary)
    
    def __lt__(self, other):
        return self.central.slope_to(self.secondary) < other.central.slope_to(other.secondary)
    
    def __repr__(self):
        return str(self.central.slope_to(self.secondary))


class LineSegment():
    def __init__(self, a: Point2D, b: Point2D):
        self.a = a
        self.b = b
        
    def __repr__(self):
        return str(self.a) + " -> " + str(self.b)
    
    def draw(self):
        plt.plot([self.a.x, self.b.x], [self.a.y, self.b.y])
        return None


def BruteCollinearPoints(points: List[Point2D]):
    """
    Examines 4 points at at a time
    Checks whether all 4 points lie on the same
    line, returning all such line segments
    """
    segments = []
    for p in range(0, len(points)):
        pp = points[p]
        for q in range(p + 1, len(points)):
            pq = points[q]
            for r in range(q + 1, len(points)):
                pr = points[r]
                if pp.slope_to(pq) == pp.slope_to(pr):
                    for s in range(r + 1, len(points)):
                        ps = points[s]
                        if pp.slope_to(pq) == pp.slope_to(ps):
                            min_point = min([pp, pq, pr, ps])
                            max_point = max([pp, pq, pr, ps])
                            segments.append(LineSegment(min_point, max_point))
    return segments


def FastCollinearPoints(points: List[Point2D]):
    mergesort(points)
    segments = []
    for p in points:
        slopes = [Ordered_Slopes(p, r) for r in points if r != p]
        mergesort(slopes)
        s_idx = 0
        while s_idx < (len(slopes) - 3):
            if slopes[s_idx] == slopes[s_idx + 1]:
                n_coll = 2
                while s_idx < (len(slopes) - 1) and slopes[s_idx] == slopes[s_idx + 1]:
                    n_coll += 1
                    s_idx += 1
                if 3 < n_coll:
                    segments.append(LineSegment(slopes[s_idx].central, slopes[s_idx].secondary))
            s_idx += 1
    return segments


if __name__ == "__main__":
    with open('kw1260.txt', 'r') as f:
        next(f)
        points = []
        for line in f:
            coords = [int(coord) for coord in line.split()]
            points.append(Point2D(coords[0], coords[1]))

    segments = FastCollinearPoints(points)

    for p in points:
        p.draw()

    for s in segments:
        s.draw()

    plt.show()
