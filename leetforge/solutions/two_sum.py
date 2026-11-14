"""LeetCode 1 - Two Sum"""
META = {"id": 1, "title": "Two Sum", "difficulty": "Easy", "tags": ["array", "hash-table"],
        "pattern": "Hash map of complements"}


def brute_force(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def hash_map(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []


APPROACHES = {"brute_force": brute_force, "hash_map": hash_map}
COMPLEXITY = {"brute_force": ("O(n^2)", "O(1)"), "hash_map": ("O(n)", "O(n)")}
TESTS = [(([2, 7, 11, 15], 9), [0, 1]), (([3, 2, 4], 6), [1, 2]), (([3, 3], 6), [0, 1]), (([-1, -2, -3, -4, -5], -8), [2, 4])]


def CHECK(args, out):          # several valid answers may exist
    nums, target = args
    return len(out) == 2 and out[0] != out[1] and all(0 <= i < len(nums) for i in out) \
        and nums[out[0]] + nums[out[1]] == target


def gen(n, rng):
    nums = list(range(n))
    return nums, nums[-1] + nums[-2]      # answer sits at the end: worst case for the scan


def rand_case(rng):
    n = rng.randint(2, 8)
    nums = [rng.randint(-5, 5) for _ in range(n)]
    i, j = rng.sample(range(n), 2)
    return nums, nums[i] + nums[j]
