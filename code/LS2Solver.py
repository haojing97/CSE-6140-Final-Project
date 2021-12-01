import random
import time
from BaseSolver import BaseSolver


class LS2Solver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.not_improve = 0
        self.max_not_improve = 16

        self.cur_route = []
        self.cur_cost = 0
        self.best_neighbor_route = []
        self.best_neighbor_cost = 0

    def init_route(self):
        self.cur_route = random.sample(
            range(self.size), self.size)
        self.cur_cost = self.get_cost(self.cur_route)
        return

    def find_best_neighbor(self):
        return

    def update(self):
        if self.best_neighbor_cost < self.cur_cost:
            self.cur_route = self.best_neighbor_route
            self.cur_cost = self.best_neighbor_cost
            self.sol = self.cur_cost
            self.route = self.cur_route
            self.not_improve = 0
        else:
            self.not_improve += 1

    def solve(self, cutoff, seed):
        super().solve(cutoff, seed)
        self.init_route()
        while self.not_improve < self.max_not_improve:
            if time.time() > cutoff + self.start:
                break
            self.find_best_neighbor()
            self.update()
        return
