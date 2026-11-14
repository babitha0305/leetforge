"""LeetCode 300 - Longest Increasing Subsequence"""
from bisect import bisect_left

META = {"id": 300, "title": "Longest Increasing Subsequence", "difficulty": "Medium", "tags": ["dp", "binary-search"],
        "pattern": "DP over prefixes / patience sorting"}


def dp_quadratic(nums):
    best = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best, default=0)


def patience_sorting(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


APPROACHES = {"dp_quadratic": dp_quadratic, "patience_sorting": patience_sorting}
COMPLEXITY = {"dp_quadratic": ("O(n^2)", "O(n)"), "patience_sorting": ("O(n log n)", "O(n)")}
TESTS = [(([10, 9, 2, 5, 3, 7, 101, 18],), 4), (([0, 1, 0, 3, 2, 3],), 4), (([7, 7, 7, 7],), 1), (([],), 0), (([1, 2, 3, 4],), 4)]


def gen(n, rng):
    return ([rng.randint(0, 10 * n) for _ in range(n)],)


def rand_case(rng):
    return ([rng.randint(0, 5) for _ in range(rng.randint(0, 9))],)
