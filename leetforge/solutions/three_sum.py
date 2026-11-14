"""LeetCode 15 - 3Sum"""
from itertools import combinations

META = {"id": 15, "title": "3Sum", "difficulty": "Medium", "tags": ["two-pointers", "sorting", "array"],
        "pattern": "Sort, fix one, two pointers for the rest"}


def brute_force(nums):
    found = {tuple(sorted(c)) for c in combinations(nums, 3) if sum(c) == 0}
    return [list(t) for t in sorted(found)]


def two_pointers(nums):
    nums = sorted(nums)
    res = []
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
    return res


def NORMALIZE(out):
    return sorted(sorted(t) for t in out)


APPROACHES = {"brute_force": brute_force, "two_pointers": two_pointers}
COMPLEXITY = {"brute_force": ("O(n^3)", "O(n)"), "two_pointers": ("O(n^2)", "O(1)")}
TESTS = [(([-1, 0, 1, 2, -1, -4],), [[-1, -1, 2], [-1, 0, 1]]), (([0, 1, 1],), []), (([0, 0, 0],), [[0, 0, 0]]),
         (([0, 0, 0, 0],), [[0, 0, 0]]), (([],), [])]
BENCH_SIZES = [16, 24, 32, 48, 64, 96, 128]


def gen(n, rng):
    return ([rng.randint(-n, n) for _ in range(n)],)


def rand_case(rng):
    return ([rng.randint(-3, 3) for _ in range(rng.randint(0, 8))],)
