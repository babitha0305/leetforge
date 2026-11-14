"""LeetCode 3 - Longest Substring Without Repeating Characters"""
META = {"id": 3, "title": "Longest Substring Without Repeating Characters", "difficulty": "Medium",
        "tags": ["sliding-window", "hash-table", "string"], "pattern": "Sliding window with last-seen index"}


def brute_force(s):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
        best = max(best, len(seen))
    return best


def sliding_window(s):
    last, start, best = {}, 0, 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best


APPROACHES = {"brute_force": brute_force, "sliding_window": sliding_window}
COMPLEXITY = {"brute_force": ("O(n^2)", "O(n)"), "sliding_window": ("O(n)", "O(n)")}
TESTS = [(("abcabcbb",), 3), (("bbbbb",), 1), (("pwwkew",), 3), (("",), 0), (("abba",), 2)]


def gen(n, rng):
    return ("".join(chr(0x4E00 + i) for i in range(n)),)      # all-unique: quadratic worst case for brute force


def rand_case(rng):
    return ("".join(rng.choice("abc") for _ in range(rng.randint(0, 10))),)
