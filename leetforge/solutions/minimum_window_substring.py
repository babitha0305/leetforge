"""LeetCode 76 - Minimum Window Substring"""
from collections import Counter

META = {"id": 76, "title": "Minimum Window Substring", "difficulty": "Hard", "tags": ["sliding-window", "hash-table", "string"],
        "pattern": "Expand right until valid, shrink left while valid"}


def brute_force(s, t):
    if not t:
        return ""
    need = Counter(t)
    for length in range(len(t), len(s) + 1):          # shortest first, leftmost wins ties
        for i in range(len(s) - length + 1):
            if not (need - Counter(s[i:i + length])):
                return s[i:i + length]
    return ""


def sliding_window(s, t):
    if not t or not s:
        return ""
    need, missing = Counter(t), len(t)
    best_start, best_end, left = 0, len(s) + 1, 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right + 1 - left < best_end - best_start:
                best_start, best_end = left, right + 1
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best_end > len(s) else s[best_start:best_end]


APPROACHES = {"brute_force": brute_force, "sliding_window": sliding_window}
COMPLEXITY = {"brute_force": ("O(n^3)", "O(m)"), "sliding_window": ("O(n + m)", "O(m)")}
TESTS = [(("ADOBECODEBANC", "ABC"), "BANC"), (("a", "a"), "a"), (("a", "aa"), ""), (("ab", "b"), "b"), (("aab", "ab"), "ab")]
BENCH_SIZES = [8, 16, 32, 48, 64, 96, 128]


def gen(n, rng):
    return "a" * n, "b"                                # never matches: brute force tries every window


def rand_case(rng):
    return "".join(rng.choice("abc") for _ in range(rng.randint(0, 8))), "".join(rng.choice("abc") for _ in range(rng.randint(0, 3)))
