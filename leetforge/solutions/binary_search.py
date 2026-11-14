"""LeetCode 704 - Binary Search"""
from bisect import bisect_left

META = {"id": 704, "title": "Binary Search", "difficulty": "Easy", "tags": ["array", "binary-search"],
        "pattern": "Halve the search interval"}


def linear_scan(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1


def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def bisect_lib(nums, target):
    i = bisect_left(nums, target)
    return i if i < len(nums) and nums[i] == target else -1


APPROACHES = {"linear_scan": linear_scan, "binary_search": binary_search, "bisect_lib": bisect_lib}
COMPLEXITY = {"linear_scan": ("O(n)", "O(1)"), "binary_search": ("O(log n)", "O(1)"), "bisect_lib": ("O(log n)", "O(1)")}
TESTS = [(([-1, 0, 3, 5, 9, 12], 9), 4), (([-1, 0, 3, 5, 9, 12], 2), -1), (([5], 5), 0), (([], 1), -1), (([1, 3], 3), 1)]


def gen(n, rng):
    return list(range(n)), n - 1


def rand_case(rng):
    nums = sorted(rng.sample(range(-10, 11), rng.randint(0, 8)))
    return nums, rng.randint(-10, 10)
