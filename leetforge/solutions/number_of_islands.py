"""LeetCode 200 - Number of Islands"""
from collections import deque

META = {"id": 200, "title": "Number of Islands", "difficulty": "Medium", "tags": ["graph", "dfs", "bfs", "union-find"],
        "pattern": "Flood fill / connected components"}


def _neighbours(r, c, R, C):
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C:
            yield nr, nc


def dfs_iterative(grid):
    if not grid:
        return 0
    R, C = len(grid), len(grid[0])
    seen, islands = set(), 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1" and (r, c) not in seen:
                islands += 1
                seen.add((r, c))
                stack = [(r, c)]
                while stack:
                    cr, cc = stack.pop()
                    for nr, nc in _neighbours(cr, cc, R, C):
                        if grid[nr][nc] == "1" and (nr, nc) not in seen:
                            seen.add((nr, nc))
                            stack.append((nr, nc))
    return islands


def bfs(grid):
    if not grid:
        return 0
    R, C = len(grid), len(grid[0])
    seen, islands = set(), 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1" and (r, c) not in seen:
                islands += 1
                seen.add((r, c))
                q = deque([(r, c)])
                while q:
                    cr, cc = q.popleft()
                    for nr, nc in _neighbours(cr, cc, R, C):
                        if grid[nr][nc] == "1" and (nr, nc) not in seen:
                            seen.add((nr, nc))
                            q.append((nr, nc))
    return islands


def union_find(grid):
    if not grid:
        return 0
    R, C = len(grid), len(grid[0])
    parent = list(range(R * C))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    count = sum(cell == "1" for row in grid for cell in row)
    for r in range(R):
        for c in range(C):
            if grid[r][c] != "1":
                continue
            for nr, nc in ((r + 1, c), (r, c + 1)):
                if nr < R and nc < C and grid[nr][nc] == "1":
                    a, b = find(r * C + c), find(nr * C + nc)
                    if a != b:
                        parent[a] = b
                        count -= 1
    return count


APPROACHES = {"dfs_iterative": dfs_iterative, "bfs": bfs, "union_find": union_find}
COMPLEXITY = {"dfs_iterative": ("O(n)", "O(n)"), "bfs": ("O(n)", "O(n)"), "union_find": ("O(n)", "O(n)")}   # n = cells
TESTS = [((["11110", "11010", "11000", "00000"],), 1), ((["11000", "11000", "00100", "00011"],), 3), (([],), 0),
         ((["1", "0", "1"],), 2)]


def gen(n, rng):
    side = max(1, int(n ** 0.5))
    return (["".join(rng.choice("01") for _ in range(side)) for _ in range(side)],)


def rand_case(rng):
    R, C = rng.randint(1, 4), rng.randint(1, 4)
    return (["".join(rng.choice("01") for _ in range(C)) for _ in range(R)],)
