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

        return route, dist
    
    # Get the MST total distance based on Prim algorithm
    def mst(self, not_seen):
        m = [[] for _ in range(len(self.matrix))]
        for i in not_seen:
            for j in not_seen:
                if i != j:
                    heapq.heappush(m[i], (self.matrix[i][j], j))
        
        cur = random.choice(list(not_seen))
        distance = 0
        seen = set()

        for _ in range(len(not_seen)-1):
            tmp = float('inf')
            tmp_node = -1
            if len(not_seen) == 1:
                last = list(not_seen)[0]
                for j in seen:
                    if self.matrix[j][last] < tmp:
                        tmp = self.matrix[j][last]
                distance += tmp
                break
            if cur in seen: continue
            seen.add(cur)
            not_seen.discard(cur)
            '''
            for next_node in not_seen:
                for i in seen:
                    if self.matrix[i][next_node] < tmp:
                        tmp = self.matrix[i][next_node]
                        tmp_node = next_node
            '''
            pair = []
            for i in seen:
                if len(m[i]) == 0: continue
                while len(m[i]) and m[i][0][1] in seen:
                    heapq.heappop(m[i])
                if len(m[i]) == 0: continue
                if m[i][0][0] < tmp:
                    tmp = m[i][0][0]
                    tmp_node = m[i][0][1]
                    pair.extend([i, tmp_node])
            heapq.heappop(m[pair[0]])
            cur = tmp_node
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

    def solve(self, cutoff, seed):
        super().solve(cutoff, seed)
        n = len(self.matrix)
        node = Node([0], self.matrix)
        self.route, self.sol = self.get_upper_bound(node)
        self.record_trace()
        node.lower_bound = self.get_lower_bound(node)
        q = [node]
        heapq.heapify(q)
        while q:
            cur = heapq.heappop(q)
            if cur.lower_bound < self.sol:
                if len(cur.path) < n - 1:
                    cur_path = cur.path[:]
                    for i in range(n):
                        if i not in cur.path:
                            cur_path.append(i)
                            new_node = Node(cur_path[:], self.matrix)
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
                    cur_dist = cur.get_cur_distance() + self.matrix[cur.path[0]][cur.path[-1]]
                    if cur_dist < self.sol:
                        self.sol = cur_dist
                        self.route = cur.path
                        self.record_trace()


if __name__ == '__main__':
    bnb = BnBSolver()
    bnb.matrix = [[0,2,3,1,2], [2,0,4,6,10], [3,4,0,2,9], [1,6,2,0,5], [2,10,9,5,0]]
    #bnb.matrix = [[0,2,3],[2,0,1],[3,1,0]]
    not_seen = set([0,1,2,3,4])
    print(bnb.mst(not_seen))