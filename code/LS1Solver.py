'''
Implementation of the SA algorithm.
'''
import math
import random
import time
from BaseSolver import BaseSolver

# LS1Solver is the a simulated annealing solver.


class LS1Solver(BaseSolver):
    def __init__(self):
        super().__init__()

        self.restart = 16  # restart times
        self.temp = 0
        self.param = 0

        self.cur_route = []
        self.cur_cost = float('inf')
        self.next_route = []
        self.next_cost = float('inf')

    # initialize temperature and annealing parameter
    def init_temp(self):
        self.temp = 1e8
        self.param = 0.999

    # randomly pick up a permutation as the initial route
    def init_route(self):
        self.cur_route = random.sample(
            range(self.size), self.size)
        self.cur_cost = self.get_cost(self.cur_route)
        self.next_route = []
        self.next_cost = float('inf')
        return

    def get_cost(self, route):
        res = 0
        n = len(route)
        for i in range(n):
            res += self.matrix[route[i - 1]][route[i]]
        return res

    # the probability of moving to the next route
    def pr(self):
        delta = self.next_cost - self.cur_cost
        if delta <= 0:
            return 1
        else:
            return math.exp(-delta / self.temp)

    # using 2-opt to generate the next route
    def generate_next(self):
        while True:
            i = random.randint(0, self.size)
            j = random.randint(0, self.size)
            if abs(i - j) > 2:
                break
        if i > j:
            j, i = i, j

        self.next_route = self.cur_route[:i] + \
            self.cur_route[i:j][::-1] + self.cur_route[j:]
        self.next_cost = self.get_cost(self.next_route)

    # decide whether to move to the next route or not, if so, update relevant variables.
    def update(self):
        should_update = True
        pr = self.pr()
        if pr < 1:
            should_update = pr > random.random()
        if should_update:
            self.cur_route = self.next_route
            self.cur_cost = self.next_cost
            if self.cur_cost < self.sol:
                self.sol = self.cur_cost
                self.route = self.cur_route[:]
                self.record_trace()

    def cooling(self):
        self.temp *= self.param

    def solve(self, cutoff, seed):
        super().solve(cutoff, seed)
        for _ in range(self.restart):
            self.init_temp()
            self.init_route()
            while self.temp > 1e-9:
                if time.time() >= cutoff + self.start:
                    break
                self.generate_next()
                self.update()
                self.cooling()
