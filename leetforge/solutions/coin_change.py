"""LeetCode 322 - Coin Change"""
META = {"id": 322, "title": "Coin Change", "difficulty": "Medium", "tags": ["dp", "bfs"],
        "pattern": "Unbounded knapsack / shortest path over amounts"}


def bottom_up(coins, amount):
    inf = amount + 1
    dp = [0] + [inf] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] <= amount else -1


def bfs(coins, amount):
    if amount == 0:
        return 0
    seen, frontier, steps = {0}, [0], 0
    while frontier:
        steps += 1
        nxt = []
        for x in frontier:
            for c in coins:
                y = x + c
                if y == amount:
                    return steps
                if y < amount and y not in seen:
                    seen.add(y)
                    nxt.append(y)
        frontier = nxt
    return -1


APPROACHES = {"bottom_up": bottom_up, "bfs": bfs}
COMPLEXITY = {"bottom_up": ("O(amount * coins)", "O(amount)"), "bfs": ("O(amount * coins)", "O(amount)")}
TESTS = [(([1, 2, 5], 11), 3), (([2], 3), -1), (([1], 0), 0), (([186, 419, 83, 408], 6249), 20), (([2, 5, 10, 1], 27), 4)]


def gen(n, rng):
    return [1, 5, 10, 25, 50, 100], n


def rand_case(rng):
    return rng.sample(range(1, 8), rng.randint(1, 3)), rng.randint(0, 20)
