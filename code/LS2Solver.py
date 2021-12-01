import random
import time
from BaseSolver import BaseSolver

# LS2Solver is a hill climbing solver.


class LS2Solver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.restart = 16
        self.cur_route = []
        self.cur_cost = float('inf')
        self.best_neighbor_route = []
        self.best_neighbor_cost = float('inf')

    def init_route(self):
        self.cur_route = random.sample(
            range(self.size), self.size)
        self.cur_cost = self.get_cost(self.cur_route)
        self.best_neighbor_route = []
        self.best_neighbor_cost = float('inf')
        return

    def get_cost(self, route):
        res = 0
        n = len(route)
        for i in range(n):
            res += self.matrix[route[i - 1]][route[i]]
        return res

    def find_best_neighbor(self):
        for i in range(self.size - 2):
            for j in range(i + 2, min(self.size, self.size - 1 + i)):
                new_route = self.cur_route[:i] + \
                    self.cur_route[i:j][::-1] + self.cur_route[j:]
                new_cost = self.get_cost(new_route)
                if new_cost < self.best_neighbor_cost:
                    self.best_neighbor_cost = new_cost
                    self.best_neighbor_route = new_route

        return

    def update(self):
        self.cur_route = self.best_neighbor_route
        self.cur_cost = self.best_neighbor_cost
        self.sol = self.cur_cost
        self.route = self.cur_route
        self.record_trace()

    def solve(self, cutoff, seed):
        super().solve(cutoff, seed)
        for _ in range(self.restart):
            self.init_route()
            while True:
                if time.time() > cutoff + self.start:
                    break
                self.find_best_neighbor()
                if self.best_neighbor_cost >= self.cur_cost:
                    break
                self.update()
        return
