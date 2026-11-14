"""LeetCode 49 - Group Anagrams"""
from collections import defaultdict

META = {"id": 49, "title": "Group Anagrams", "difficulty": "Medium", "tags": ["hash-table", "string", "sorting"],
        "pattern": "Canonical key per group"}


def sorted_key(strs):
    groups = defaultdict(list)
    for w in strs:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())


def count_key(strs):
    groups = defaultdict(list)
    for w in strs:
        counts = [0] * 26
        for ch in w:
            counts[ord(ch) - 97] += 1
        groups[tuple(counts)].append(w)
    return list(groups.values())


def NORMALIZE(out):
    return sorted(sorted(g) for g in out)


APPROACHES = {"sorted_key": sorted_key, "count_key": count_key}
COMPLEXITY = {"sorted_key": ("O(n * k log k)", "O(n * k)"), "count_key": ("O(n * k)", "O(n * k)")}
TESTS = [((["eat", "tea", "tan", "ate", "nat", "bat"],), [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
         (([""],), [[""]]), ((["a"],), [["a"]])]


def gen(n, rng):
    return ([''.join(rng.choice("abcdefghij") for _ in range(6)) for _ in range(n)],)


def rand_case(rng):
    return ([''.join(rng.choice("abc") for _ in range(rng.randint(0, 3))) for _ in range(rng.randint(1, 8))],)
