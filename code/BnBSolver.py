from BaseSolver import BaseSolver
import copy
import random
import heapq

class Node:
    def __init__(self, path, matrix):
        self.path = copy.deepcopy(path)
        self.lower_bound = 0
        self.m = matrix 

    def get_cur_distance(self):
        dist = 0
        for i in range(len(self.path)-1):
            dist += self.m[self.path[i]][self.path[i+1]]
        return dist

    def __lt__(self, cmp):
        return True if self.lower_bound < cmp.lower_bound else False
        
class BnBSolver(BaseSolver):
    def __init__(self):
        super().__init__()
    
    def get_upper_bound(self, node):
        n = len(self.matrix)
        dist = node.get_cur_distance()
        for _ in range(n-1):
            last = node.path[-1]
            tmp = float('inf')
            next_node = -1
            for j in range(n):
                if j not in node.path and tmp > self.matrix[last][j]:
                    tmp = self.matrix[last][j]
                    next_node = j
            node.path.append(next_node)
            dist += tmp
        
        last = node.path[-1]
        route = node.path[:]
        node.path = node.path[:1]
        dist += self.matrix[last][0]
        print(dist)
        return route, dist
    
    # Get the MST total distance based on Prim algorithm
    def mst(self, not_seen):
        self.src = random.choice(list(not_seen))
        
        q = [self.src]
        distance = 0

        for _ in range(len(not_seen)-1):
            tmp = float('inf')
            tmp_node = -1
            cur = q.pop(0)
            if cur not in not_seen: continue
            not_seen.discard(cur)

            for next_node in not_seen:
                if self.matrix[cur][next_node] < tmp:
                    tmp = self.matrix[cur][next_node]
                    tmp_node = next_node

            q.append(tmp_node)
            distance += tmp
        
        return distance

    # Algorithm to calculate the lower bound
    def get_lower_bound(self, node):
        dist = node.get_cur_distance()
        seen = set(node.path)
        all_nodes = set([i for i in range(len(self.matrix))])
        not_seen = all_nodes.difference(seen)
        cur_shortest = float('inf')
        for i in seen:
            for j in not_seen:
                if self.matrix[i][j] < cur_shortest:
                    cur_shortest = self.matrix[i][j]
        dist += cur_shortest
        dist += self.mst(not_seen)
        
        return dist

    def solve(self, time, seed):
        super().solve(time, seed)
        n = len(self.matrix)
        node = Node([random.randint(0, n-1)], self.matrix)
        self.route, self.sol = self.get_upper_bound(node)
        self.record_trace()
        node.lower_bound = self.get_lower_bound(node)
        q = [node]
        heapq.heapify(q)

        while q:
            cur = heapq.heappop(q)
            if cur.lower_bound >= self.sol: continue
            else:
                if len(cur.path) < n - 1:
                    cur_path = cur.path[:]
                    for i in range(n):
                        if i not in cur.path:
                            cur_path.append(i)
                            new_node = Node(copy.deepcopy(cur_path), self.matrix)
                            cur_bound = self.get_lower_bound(new_node)
                            if cur_bound < self.sol:
                                new_node.lower_bound = cur_bound
                                heapq.heappush(q, new_node)
                            cur_path.pop()
                else:
                    x = list(i for i in range(n))
                    diff = [item for item in x if item not in cur.path]
                    last_node = diff[0]
                    cur.path.append(last_node)
                    cur_dist = cur.get_cur_distance() + self.matrix[0][cur.path[-1]]
                    if cur_dist < self.sol:
                        self.sol = cur_dist
                        self.route = cur.path
                        self.record_trace()
