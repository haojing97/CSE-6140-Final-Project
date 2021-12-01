'''
Implementation of the MST-APPROX algorithm based on Minimum Spanning Tree.
'''
from BaseSolver import BaseSolver
import heapq
import random

class ApproxSolver(BaseSolver):
    def __init__(self):
        super().__init__()

    # Prim's algorithm
    # Get one route based on the following algorithm:
    # Start with some root node s greedily grow a tree T from s outward.
    # At each step, add the cheapest edge e to T that has exactly one endpoint in T.
    def prim(self):
        n = len(self.matrix)
        self.adjacent = [[] for _ in range(n)]
        self.src = random.randint(0, len(self.matrix)-1)

        # Min heap to help add cheapest edge to T that has exactly one endpoint in T
        q = [(0, self.src, None)]
        heapq.heapify(q)
        seen = set()
        while q:
            _, node, par = heapq.heappop(q)
            if node in seen: continue
            seen.add(node)
            if par != None:
                self.adjacent[par].append(node)
            for next_node in range(n):
                if next_node not in seen:
                    heapq.heappush(q, (self.matrix[node][next_node], next_node, node))

    # Find the cycle using DFS
    def dfs(self, par):
        temp = [par]
        for child in self.adjacent[par]:
            temp.extend(self.dfs(child))
        return temp[:]

    def solve(self, cutoff, seed):
        super().solve(cutoff, seed)
        self.sol = 0
        self.prim()
        #Form a complete cycle
        self.route = self.dfs(self.src)
        self.route.extend([self.src])
        # Calculate distance
        for i in range(len(self.route)-1):
            self.sol += self.matrix[self.route[i]][self.route[i+1]]
        self.record_trace()