"""LeetCode 20 - Valid Parentheses"""
META = {"id": 20, "title": "Valid Parentheses", "difficulty": "Easy", "tags": ["stack", "string"],
        "pattern": "Stack of open brackets"}


def stack(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    st = []
    for ch in s:
        if ch in pairs:
            if not st or st.pop() != pairs[ch]:
                return False
        else:
            st.append(ch)
    return not st


def repeated_replace(s):
    while "()" in s or "[]" in s or "{}" in s:
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""


APPROACHES = {"repeated_replace": repeated_replace, "stack": stack}
COMPLEXITY = {"repeated_replace": ("O(n^2)", "O(n)"), "stack": ("O(n)", "O(n)")}
TESTS = [(("()",), True), (("()[]{}",), True), (("(]",), False), (("([)]",), False), (("{[]}",), True), (("(",), False), (("",), True)]


def gen(n, rng):
    return ("(" * (n // 2) + ")" * (n // 2),)


def rand_case(rng):
    return ("".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 8))),)
