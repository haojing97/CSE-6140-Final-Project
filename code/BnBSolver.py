from BaseSolver import BaseSolver
import copy
import random
import heapq
import time


class Node:
    def __init__(self, path=[0]):
        self.path = copy.deepcopy(path)
        self.lower_bound = 0

    def __lt__(self, cmp):
        return True if self.lower_bound < cmp.lower_bound else False


class BnBSolver(BaseSolver):
    def __init__(self):
        super().__init__()

    def get_upper_bound(self, node):
        n = len(self.matrix)
        dist = self.get_cur_distance(node.path)
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

    def get_cur_distance(self, path):
        dist = 0
        for i in range(len(path)-1):
            dist += self.matrix[path[i]][path[i+1]]
        return dist

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
            if cur in seen:
                continue
            seen.add(cur)
            not_seen.discard(cur)

            src = -1
            for i in seen:
                if len(m[i]) == 0:
                    continue
                while len(m[i]) and m[i][0][1] in seen:
                    heapq.heappop(m[i])
                if len(m[i]) == 0:
                    continue
                if m[i][0][0] < tmp:
                    tmp = m[i][0][0]
                    tmp_node = m[i][0][1]
                    src = i

            heapq.heappop(m[src])
            cur = tmp_node
            distance += tmp

        return distance

    # Algorithm to calculate the lower bound
    def get_lower_bound(self, node):
        dist = self.get_cur_distance(node.path)
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
        node = Node()
        self.route, self.sol = self.get_upper_bound(node)
        self.record_trace()
        node.lower_bound = self.get_lower_bound(node)
        q = [node]
        heapq.heapify(q)
        while q:
            if time.time() - self.start > cutoff:
                return
            cur = heapq.heappop(q)
            if cur.lower_bound < self.sol:
                if len(cur.path) < n - 1:
                    cur_path = cur.path[:]
                    for i in range(n):
                        if i not in cur.path:
                            cur_path.append(i)
                            new_node = Node(cur_path[:])
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
                    cur_dist = self.get_cur_distance(
                        cur.path) + self.matrix[cur.path[0]][cur.path[-1]]
                    if cur_dist < self.sol:
                        self.sol = cur_dist
                        self.route = cur.path
                        self.record_trace()


if __name__ == '__main__':
    bnb = BnBSolver()
    bnb.matrix = [[0, 2, 3, 1, 2], [2, 0, 4, 6, 10], [
        3, 4, 0, 2, 9], [1, 6, 2, 0, 5], [2, 10, 9, 5, 0]]
    # bnb.matrix = [[0,2,3],[2,0,1],[3,1,0]]
    bnb.matrix = [[0, 106843, 117658, 645878, 265944, 438678, 35813, 366652, 147037, 426728, 240239, 184937, 128129, 342599, 428931, 447299, 129857, 254940, 501038, 271352], [106843, 0, 14476, 539964, 159909, 359663, 108023, 263495, 80787, 320126, 138522, 130798, 37435, 236056, 327969, 340794, 23709, 153710, 407787, 171932], [117658, 14476, 0, 528307, 151699, 360444, 121297, 250601, 89283, 310748, 133737, 139105, 43996, 224991, 314617, 331556, 20583, 140190, 393612, 167890], [645878, 539964, 528307, 0, 390281, 451540, 646358, 283583, 540328, 238337, 428716, 547874, 529291, 304516, 234495, 223221, 518330, 394451, 238490, 412357], [265944, 159909, 151699, 390281, 0, 255155, 260122, 141056, 150560, 161269, 43367, 166758, 141281, 90180, 208026, 181574, 136366, 90145, 307623, 53722], [438678, 359663, 360444, 451540, 255155, 0, 414083, 347241, 292449, 253563, 239968, 255761, 323743, 287666, 393836, 254686, 339883, 344675, 496986, 207524], [35813, 108023, 121297, 646358, 260122, 414083, 0, 371498, 126907, 421327, 229782, 158459, 118893, 341872, 435897, 441428, 128260, 261487, 513440, 258500], [366652, 263495, 250601, 283583, 141056, 347241, 371498, 0, 282998, 125856, 184322, 306466, 260358, 61570, 67784, 142711, 244009, 112034, 167249, 187296], [147037, 80787, 89283, 540328, 150560, 292449, 126907, 282998, 0, 306765, 112115, 50022, 45505, 239837, 350673, 325709, 72873, 187850, 442465, 135610], [426728, 320126, 310748, 238337, 161269, 253563, 421327, 125856, 306765, 0, 194742, 310281, 302439, 95892, 148150, 21151, 296880, 199410, 246240, 174881], [
        240239, 138522, 133737, 428716, 43367, 239968, 229782, 184322, 112115, 194742, 0, 123742, 112237, 132771, 251388, 213922, 115113, 119432, 350559, 34793], [184937, 130798, 139105, 547874, 166758, 255761, 158459, 306466, 50022, 310281, 123742, 0, 95140, 256511, 374040, 327515, 121849, 222363, 470722, 135531], [128129, 37435, 43996, 529291, 141281, 323743, 118893, 260358, 45505, 302439, 112237, 95140, 0, 225006, 326972, 322539, 27808, 156598, 413345, 143337], [342599, 236056, 224991, 304516, 90180, 287666, 341872, 61570, 239837, 95892, 132771, 256511, 225006, 0, 122602, 116686, 214017, 103707, 226412, 129569], [428931, 327969, 314617, 234495, 208026, 393836, 435897, 67784, 350673, 148150, 251388, 374040, 326972, 122602, 0, 157592, 309445, 174488, 105167, 251920], [447299, 340794, 331556, 223221, 181574, 254686, 441428, 142711, 325709, 21151, 213922, 327515, 322539, 116686, 157592, 0, 317482, 220323, 251316, 192572], [129857, 23709, 20583, 518330, 136366, 339883, 128260, 244009, 72873, 296880, 115113, 121849, 27808, 214017, 309445, 317482, 0, 136280, 392335, 148815], [254940, 153710, 140190, 394451, 90145, 344675, 261487, 112034, 187850, 199410, 119432, 222363, 156598, 103707, 174488, 220323, 136280, 0, 256748, 142430], [501038, 407787, 393612, 238490, 307623, 496986, 513440, 167249, 442465, 246240, 350559, 470722, 413345, 226412, 105167, 251316, 392335, 256748, 0, 354491], [271352, 171932, 167890, 412357, 53722, 207524, 258500, 187296, 135610, 174881, 34793, 135531, 143337, 129569, 251920, 192572, 148815, 142430, 354491, 0]]
    not_seen = set(i for i in range(20))
    print(bnb.mst(not_seen))
