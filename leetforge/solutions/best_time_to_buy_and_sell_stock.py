"""LeetCode 121 - Best Time to Buy and Sell Stock"""
META = {"id": 121, "title": "Best Time to Buy and Sell Stock", "difficulty": "Easy", "tags": ["array", "dp"],
        "pattern": "Track running minimum"}


def brute_force(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best


def one_pass(prices):
    lowest, best = float("inf"), 0
    for p in prices:
        lowest = min(lowest, p)
        best = max(best, p - lowest)
    return best


APPROACHES = {"brute_force": brute_force, "one_pass": one_pass}
COMPLEXITY = {"brute_force": ("O(n^2)", "O(1)"), "one_pass": ("O(n)", "O(1)")}
TESTS = [(([7, 1, 5, 3, 6, 4],), 5), (([7, 6, 4, 3, 1],), 0), (([1],), 0), (([2, 4, 1],), 2), (([],), 0)]


def gen(n, rng):
    return ([rng.randint(1, 10_000) for _ in range(n)],)


def rand_case(rng):
    return ([rng.randint(0, 9) for _ in range(rng.randint(0, 8))],)
