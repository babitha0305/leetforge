"""LeetCode 78 - Subsets"""
META = {"id": 78, "title": "Subsets", "difficulty": "Medium", "tags": ["backtracking", "bit-manipulation"],
        "pattern": "Include / exclude recursion, or bitmask enumeration"}


def backtracking(nums):
    res, cur = [], []

    def go(i):
        if i == len(nums):
            res.append(cur[:])
            return
        go(i + 1)
        cur.append(nums[i])
        go(i + 1)
        cur.pop()

    go(0)
    return res


def bitmask(nums):
    n = len(nums)
    return [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]


def NORMALIZE(out):
    return sorted(sorted(s) for s in out)


APPROACHES = {"backtracking": backtracking, "bitmask": bitmask}
COMPLEXITY = {"backtracking": ("O(n * 2^n)", "O(n)"), "bitmask": ("O(n * 2^n)", "O(1)")}   # excl. output
TESTS = [(([1, 2, 3],), [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]), (([0],), [[], [0]]), (([],), [[]])]
BENCH_SIZES = [4, 6, 8, 10, 12, 14, 16]


def gen(n, rng):
    return (list(range(n)),)


def rand_case(rng):
    return (rng.sample(range(-5, 6), rng.randint(0, 5)),)
