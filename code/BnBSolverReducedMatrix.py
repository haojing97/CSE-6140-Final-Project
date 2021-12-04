import heapq
import copy
from math import cos
from BaseSolver import BaseSolver


class Node:
    def __init__(self, path, matrix, level, i, j) -> None:
        self.path = path
        self.matrix = matrix

        n = len(self.matrix)
        if level != 0:
            for k in range(n):
                self.matrix[i][k] = self.matrix[k][j] = float('inf')
        self.matrix[j][0] = float('inf')
        self.level = level
        self.path.append(j)
        self.vertex = j

        self.cost = 0

    def __lt__(self, cmp):
        return self.cost < cmp.cost


def cost_calculation(matrix):
    cost = 0
    n = len(matrix)
    row = [float('inf')] * n
    col = [float('inf')] * n
    reduce_row(matrix, row)
    reduce_col(matrix, col)

    cost += sum([x for x in row if x != float('inf')])
    cost += sum([x for x in col if x != float('inf')])
    return cost


def reduce_col(matrix, col):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < col[j]:
                col[j] = matrix[i][j]

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != float('inf') and col[j] != float('inf'):
                matrix[i][j] -= col[j]


def reduce_row(matrix, row):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < row[i]:
                row[i] = matrix[i][j]

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != float('inf') and row[i] != float('inf'):
                matrix[i][j] -= row[i]


class BnBSolverReducedMatrix(BaseSolver):
    def __init__(self, matrix=[]):
        super().__init__(matrix=matrix)

    def solve(self, cutoff, seed):
        super().solve(cutoff, seed)
        root = Node([], copy.deepcopy(self.matrix), 0, -1, 0)
        root.cost = cost_calculation(root.matrix)
        h = [root]

        while h:
            node = heapq.heappop(h)
            i = node.vertex
            if node.level == self.size - 1:
                self.sol = node.cost
                self.route = node.path
                return

            for j in range(self.size):
                if node.matrix[i][j] != float('inf'):
                    child = Node(copy.deepcopy(node.path), copy.deepcopy(node.matrix),
                                 node.level + 1, i, j)
                    child.cost = node.cost + \
                        node.matrix[i][j] + \
                        cost_calculation(child.matrix)
                    heapq.heappush(h, child)


if __name__ == '__main__':
    matrix = [
        [float('inf'), 20, 30, 10, 11],
        [15, float('inf'), 16, 4, 2],
        [3, 5, float('inf'), 2, 4],
        [19, 6, 18, float('inf'), 3],
        [16, 4, 7, 16, float('inf')]
    ]
    s = BnBSolver(matrix)
    s.solve(100, 0)
