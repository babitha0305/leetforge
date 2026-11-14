"""LeetCode 207 - Course Schedule"""
from collections import deque

META = {"id": 207, "title": "Course Schedule", "difficulty": "Medium", "tags": ["graph", "topological-sort", "dfs", "bfs"],
        "pattern": "Cycle detection in a directed graph"}


def kahn_bfs(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indegree[a] += 1
    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    taken = 0
    while queue:
        x = queue.popleft()
        taken += 1
        for y in adj[x]:
            indegree[y] -= 1
            if indegree[y] == 0:
                queue.append(y)
    return taken == num_courses


def dfs_cycle(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    for a, b in prerequisites:
        adj[b].append(a)
    state = [0] * num_courses                     # 0 new, 1 on stack, 2 finished
    for start in range(num_courses):
        if state[start]:
            continue
        state[start] = 1
        stack = [(start, 0)]
        while stack:
            node, i = stack.pop()
            if i < len(adj[node]):
                stack.append((node, i + 1))
                nxt = adj[node][i]
                if state[nxt] == 1:
                    return False
                if state[nxt] == 0:
                    state[nxt] = 1
                    stack.append((nxt, 0))
            else:
                state[node] = 2
    return True


APPROACHES = {"kahn_bfs": kahn_bfs, "dfs_cycle": dfs_cycle}
COMPLEXITY = {"kahn_bfs": ("O(V + E)", "O(V + E)"), "dfs_cycle": ("O(V + E)", "O(V + E)")}
TESTS = [((2, [[1, 0]]), True), ((2, [[1, 0], [0, 1]]), False), ((1, []), True), ((3, [[1, 0], [2, 1], [0, 2]]), False),
         ((3, [[1, 1]]), False)]


def gen(n, rng):
    return n, [[i + 1, i] for i in range(n - 1)]


def rand_case(rng):
    n = rng.randint(1, 6)
    return n, [[rng.randrange(n), rng.randrange(n)] for _ in range(rng.randint(0, 8))]
