"""LeetCode 56 - Merge Intervals"""
META = {"id": 56, "title": "Merge Intervals", "difficulty": "Medium", "tags": ["sorting", "intervals", "array"],
        "pattern": "Sort by start, sweep and extend"}


def brute_force(intervals):
    items = [list(i) for i in intervals]
    merged = True
    while merged:
        merged = False
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i], items[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    items[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    del items[j]
                    merged = True
                    break
            if merged:
                break
    return sorted(items)


def sort_and_merge(intervals):
    out = []
    for start, end in sorted(intervals):
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out


def NORMALIZE(out):
    return sorted(tuple(x) for x in out)


APPROACHES = {"brute_force": brute_force, "sort_and_merge": sort_and_merge}
COMPLEXITY = {"brute_force": ("O(n^3)", "O(n)"), "sort_and_merge": ("O(n log n)", "O(n)")}
TESTS = [(([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]]), (([[1, 4], [4, 5]],), [[1, 5]]),
         (([[1, 4], [0, 4]],), [[0, 4]]), (([[1, 4], [2, 3]],), [[1, 4]])]
BENCH_SIZES = [8, 16, 32, 64, 96, 128]


def gen(n, rng):
    return ([[s, s + rng.randint(0, 5)] for s in (rng.randint(0, 10 * n) for _ in range(n))],)


def rand_case(rng):
    out = []
    for _ in range(rng.randint(1, 6)):
        s = rng.randint(0, 10)
        out.append([s, s + rng.randint(0, 4)])
    return (out,)
