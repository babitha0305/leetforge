"""LeetCode 347 - Top K Frequent Elements"""
import heapq
from collections import Counter

META = {"id": 347, "title": "Top K Frequent Elements", "difficulty": "Medium", "tags": ["heap", "hash-table", "sorting"],
        "pattern": "Count, then select top-k (heap / bucket)"}


def sort_by_count(nums, k):
    counts = Counter(nums)
    return [x for x, _ in sorted(counts.items(), key=lambda kv: -kv[1])][:k]


def heap(nums, k):
    counts = Counter(nums)
    return heapq.nlargest(k, counts, key=counts.get)


def bucket(nums, k):
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for x, c in counts.items():
        buckets[c].append(x)
    out = []
    for c in range(len(buckets) - 1, 0, -1):
        for x in buckets[c]:
            out.append(x)
            if len(out) == k:
                return out
    return out


def NORMALIZE(out):
    return sorted(out)


APPROACHES = {"sort_by_count": sort_by_count, "heap": heap, "bucket": bucket}
COMPLEXITY = {"sort_by_count": ("O(n log n)", "O(n)"), "heap": ("O(n log k)", "O(n)"), "bucket": ("O(n)", "O(n)")}
TESTS = [(([1, 1, 1, 2, 2, 3], 2), [1, 2]), (([1], 1), [1]), (([4, 4, 4, 5, 5, 6], 1), [4]), (([-1, -1, 2, 2, 2, 3], 2), [-1, 2])]


def gen(n, rng):
    return [rng.randint(0, max(1, n // 4)) for _ in range(n)], 10


def rand_case(rng):                       # unique frequencies keep the answer unambiguous
    m = rng.randint(1, 5)
    vals = rng.sample(range(-5, 6), m)
    nums = [v for v, c in zip(vals, rng.sample(range(1, m + 1), m)) for _ in range(c)]
    rng.shuffle(nums)
    return nums, rng.randint(1, m)
