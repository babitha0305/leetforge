"""LeetCode 42 - Trapping Rain Water"""
META = {"id": 42, "title": "Trapping Rain Water", "difficulty": "Hard", "tags": ["two-pointers", "array", "stack"],
        "pattern": "Water at i = min(left max, right max) - height"}


def brute_force(height):
    total = 0
    for i, h in enumerate(height):
        total += min(max(height[: i + 1]), max(height[i:])) - h
    return total


def two_pointers(height):
    lo, hi = 0, len(height) - 1
    lmax = rmax = water = 0
    while lo < hi:
        if height[lo] < height[hi]:
            lmax = max(lmax, height[lo])
            water += lmax - height[lo]
            lo += 1
        else:
            rmax = max(rmax, height[hi])
            water += rmax - height[hi]
            hi -= 1
    return water


APPROACHES = {"brute_force": brute_force, "two_pointers": two_pointers}
COMPLEXITY = {"brute_force": ("O(n^2)", "O(1)"), "two_pointers": ("O(n)", "O(1)")}
TESTS = [(([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6), (([4, 2, 0, 3, 2, 5],), 9), (([],), 0), (([3],), 0), (([2, 0, 2],), 2)]


def gen(n, rng):
    return ([rng.randint(0, 100) for _ in range(n)],)


def rand_case(rng):
    return ([rng.randint(0, 6) for _ in range(rng.randint(0, 9))],)
