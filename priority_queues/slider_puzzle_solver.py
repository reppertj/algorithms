from functools import total_ordering

from MinPQ import MinPQ

"""
Write a program to solve the 8-puzzle problem
(and its natural generalizations) using the A* search algorithm
"""


class Board():
    def __init__(self, array):
        """constructor takes an
        n x n list of lists containing
        the n ** 2 integers between 0 and n ** 2 - 1,
        where 0 represents the blank square
        """
        self.flat = [tile for row in array for tile in row]
        self.dimension = len(array)

    def __repr__(self):
        output = "\n" + str(self.dimension)
        for n in range(len(self.flat)):
            if n % (self.dimension) == 0:
                output += "\n" + str(self.flat[n])
            else:
                output += " " + str(self.flat[n])
        return output

    def hamming_distance(self):
        """Number of tiles out of place
        """
        distance = 0
        for pos in range(1, len(self.flat)):
            if pos != self.flat[pos - 1]:
                distance += 1
        return distance

    def manhattan_distance(self):
        """Sum of manhattan distances
        between self and goal
        """
        distance = 0
        for pos in range(1, len(self.flat) + 1):
            tile = self.flat[pos - 1]
            actual = ((pos - 1) // self.dimension,
                      (pos - 1) % self.dimension)
            goal = ((tile - 1) // self.dimension,
                    (tile - 1) % self.dimension)
            if tile != 0:
                distance += abs(goal[0] - actual[0]) + abs(goal[1] - actual[1])
        return distance

    def neighbors(self):
        for board in self._neighbor_boards():
            neighbor = Board([])
            neighbor.dimension = self.dimension
            neighbor.flat = board
            yield neighbor

    def _neighbor_boards(self):
        for k in range(0, len(self.flat)):
            if self.flat[k] == 0:
                pos_0 = k
                coords = ((k // self.dimension), (k % self.dimension))
                break
        neighbor_boards = []
        # horizontal neighbors
        if coords[1] == 0:
            neighbor_boards.append(self._exch(self.flat.copy(),
                                              pos_0, pos_0 + 1))
        elif coords[1] == self.dimension - 1:
            neighbor_boards.append(self._exch(self.flat.copy(),
                                              pos_0, pos_0 - 1))
        else:
            neighbor_boards.append(self._exch(self.flat.copy(),
                                              pos_0, pos_0 - 1))
            neighbor_boards.append(self._exch(self.flat.copy(),
                                              pos_0, pos_0 + 1))
        # vertical neighbors
        if coords[0] == 0:
            neighbor_boards.append(self._exch(self.flat.copy(),
                                              pos_0, pos_0 + self.dimension))
        elif coords[0] == self.dimension - 1:
            neighbor_boards.append(self._exch(self.flat.copy(),
                                              pos_0, pos_0 - self.dimension))
        else:
            neighbor_boards.append(self._exch(self.flat.copy(),
                                              pos_0, pos_0 + self.dimension))
            neighbor_boards.append(self._exch(self.flat.copy(),
                                              pos_0, pos_0 - self.dimension))
        return neighbor_boards

    @staticmethod
    def _exch(flat, a, b):
        swap = flat[a]
        flat[a] = flat[b]
        flat[b] = swap
        return flat

    def is_goal(self):
        """Is this the goal board?
        """
        for k in range(len(self.flat) - 1):
            if k + 1 != self.flat[k]:
                return False
        return True

    def __eq__(self, other):
        return (self.flat == other.flat)

    def twin(self):
        """a board that is obtained
        by exchanging any pair of tiles
        """
        for i in range(len(self.flat)):
            if self.flat[i] != 0:
                for j in range(i + 1, len(self.flat)):
                    if self.flat[j] != 0:
                        t = self._exch(self.flat.copy(), i, j)
                        break
                break
        tw = Board([])
        tw.flat = t
        tw.dimension = self.dimension
        return tw


@total_ordering
class SearchNode():
    def __init__(self, board: Board, moves: int, prev):
        self.board = board
        self.moves = moves
        self.prev = prev
        self.priority = moves + self.board.manhattan_distance()

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority


class Solver():
    def __init__(self, initial: Board):
        self.init_node = SearchNode(initial, 0, None)
        self.queue = MinPQ()
        self.queue.insert(self.init_node)
        self.twin_init = SearchNode(initial.twin(), 0, None)
        self.twin_queue = MinPQ()
        self.twin_queue.insert(self.twin_init)

    def is_solvable(self):
        return self.solution()[0] != -1

    def n_moves(self):
        return self.solution()[0]

    @staticmethod
    def seek_soln(queue):
        while True:
            min_node = queue.del_min()
            if min_node.board.is_goal():
                yield min_node
            for neighbor in min_node.board.neighbors():
                if min_node.prev is None or neighbor != min_node.prev.board:
                    queue.insert(SearchNode(
                        neighbor, min_node.moves + 1, min_node))
            yield False

    def solution(self):
        min_node = False
        impossible = False
        while min_node is False and impossible is False:
            min_node = next(self.seek_soln(self.queue))
            impossible = next(self.seek_soln(self.twin_queue))
        if not impossible:
            moves = min_node.moves
            solns = []
            while min_node.prev is not None:
                solns.append(min_node.board)
                min_node = min_node.prev
            solns.append(min_node)
            solns.reverse()
            return (moves, solns)
        else:
            return (-1, None)


sample = Board([
    [5, 2, 6],
    [3, 7, 1],
    [8, 4, 0],
])

impossible_sample = Board([
    [1, 2, 3],
    [4, 5, 6],
    [8, 7, 0],
])


s = Solver(sample)
i = Solver(impossible_sample)

print(s.solution())
print(i.solution())
