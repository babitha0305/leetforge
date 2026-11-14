"""LeetCode 238 - Product of Array Except Self"""
META = {"id": 238, "title": "Product of Array Except Self", "difficulty": "Medium", "tags": ["array", "prefix-sum"],
        "pattern": "Prefix and suffix products (no division)"}


def brute_force(nums):
    out = []
    for i in range(len(nums)):
        p = 1
        for j, x in enumerate(nums):
            if j != i:
                p *= x
        out.append(p)
    return out


def prefix_suffix(nums):
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out


APPROACHES = {"brute_force": brute_force, "prefix_suffix": prefix_suffix}
COMPLEXITY = {"brute_force": ("O(n^2)", "O(1)"), "prefix_suffix": ("O(n)", "O(1)")}
TESTS = [(([1, 2, 3, 4],), [24, 12, 8, 6]), (([-1, 1, 0, -3, 3],), [0, 0, 9, 0, 0]), (([2, 3],), [3, 2])]


def gen(n, rng):
    return ([rng.randint(-2, 2) for _ in range(n)],)


def rand_case(rng):
    return ([rng.randint(-3, 3) for _ in range(rng.randint(2, 6))],)
