# LeetForge

A professional-grade toolkit for **serious LeetCode practice** - not just a folder of solutions.
Every problem ships with multiple implementations (brute force -> optimal) and the tooling to *prove* they
are correct and as fast as claimed:

| Feature | Command | What it does |
|---|---|---|
| **Isolated test runner** | `leetforge test two-sum` | Runs each implementation in a subprocess with a hard timeout, deep-copies inputs so solutions can't corrupt test data |
| **Differential fuzzing** | `leetforge fuzz all` | Feeds random small inputs to every approach and checks they agree (or satisfy a validator). Catches bugs in "clever" optimisations against the brute-force reference |
| **Empirical complexity analysis** | `leetforge bench three-sum` | Times each approach on growing inputs, fits growth models in log-space and compares with the *declared* Big-O |
| **Spaced repetition (SM-2)** | `leetforge log two-sum --quality 4` | Schedules reviews with the SuperMemo-2 algorithm |
| **Practice coach** | `leetforge next` | Due reviews first, then new problems from your weakest topics |
| **Dashboard** | `leetforge stats` | Solved by difficulty, streak, weakest tags |
| **Scaffolding + docs** | `leetforge new ...` / `leetforge docs` | New-problem template; auto-generated [problem catalogue](docs/PROBLEMS.md) checked in CI |

Pure Python standard library - **zero runtime dependencies**.

## Quick start

```bash
git clone <your-repo-url> && cd leetforge
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

leetforge list --tag graph
leetforge test all                  # every approach of every problem
leetforge fuzz all --trials 300     # differential testing
leetforge bench subsets             # empirical complexity vs declared
leetforge next                      # what should I practise?
leetforge log two-sum --quality 4   # 0 = blackout ... 5 = perfect recall
leetforge stats
```

Example `bench` output:

```
approach      declared  estimated  slope  n range  verdict
------------  --------  ---------  -----  -------  -------
brute_force   O(n^3)    O(n^3)     3.10   16..128  match
two_pointers  O(n^2)    O(n^2)     1.86   16..128  match
```

## Problems

17 problems, 37 implementations across arrays, hashing, two pointers, sliding window, stacks,
intervals, graphs (BFS/DFS/union-find/topological sort), dynamic programming, binary search and backtracking.
See **[docs/PROBLEMS.md](docs/PROBLEMS.md)** for the full catalogue with declared time/space per approach.
IDs match LeetCode numbers; problem statements are not reproduced - only titles, tests and original solutions.

## How a problem is defined

Each file in `leetforge/solutions/` is a self-describing module:

```python
META = {"id": 1, "title": "Two Sum", "difficulty": "Easy", "tags": ["array", "hash-table"], "pattern": "..."}
APPROACHES = {"brute_force": brute_force, "hash_map": hash_map}      # first = simplest reference
COMPLEXITY = {"brute_force": ("O(n^2)", "O(1)"), "hash_map": ("O(n)", "O(n)")}
TESTS = [(([2, 7, 11, 15], 9), [0, 1]), ...]
# optional
CHECK(args, out)       # validator when several answers are valid (e.g. Two Sum)
NORMALIZE(out)         # canonical form when order doesn't matter (e.g. Group Anagrams)
gen(n, rng)            # worst-case input of size n  -> `bench`
rand_case(rng)         # small random input          -> `fuzz`
BENCH_SIZES            # custom sizes for super-linear algorithms
```

Add your own: `leetforge new longest-palindromic-substring --difficulty medium --tags string,dp`, fill in the
TODOs, then `leetforge test <slug>`, `leetforge fuzz <slug>`, `leetforge docs`.

## Design notes

- **Fuzzing beats hand-written examples.** The brute-force version is trivially correct; any optimised variant
  that disagrees on a random small input is wrong. Tests prove the harness itself catches a seeded bug.
- **Complexity estimation** fits `t ~ c * f(n)` in log-space for O(1), O(log n), O(n), O(n log n), O(n^2),
  O(n^3), O(2^n) and prefers the simplest model on near-ties. It is a *sanity check, not a proof*: timings are
  noisy, constants matter, and some classes are practically indistinguishable (O(1) vs O(log n), O(n) vs
  O(n log n)), so those are treated as compatible. Inputs come from `gen()`, so a weak generator gives a weak
  estimate - choose worst cases deliberately.
- **Isolation:** the subprocess runner uses `multiprocessing`; timeouts terminate runaway solutions. Use
  `--no-isolate` for faster in-process runs or debugging.
- **SM-2:** quality < 3 resets the interval ladder (1d) without changing ease; otherwise intervals go
  1d -> 6d -> interval x ease, with ease floored at 1.3. State lives in `.leetforge/progress.json`
  (override with `LEETFORGE_HOME`).
- **Coach:** tag score = mean latest quality over practised problems with that tag (untouched tags score 0 and
  therefore get priority); new problems are ranked by average tag weakness, then difficulty.

## Development

```bash
pytest -q                    # unit + integration tests (solutions, runner, fuzzing, complexity, SRS, CLI)
leetforge docs --check       # fails if docs/PROBLEMS.md is stale
```

CI runs the test suite, every approach, 300-case fuzzing per problem and the docs check on Python 3.9-3.12.

## Layout

```
leetforge/
  solutions/     one module per problem (tests, generators, declared complexity)
  runner.py      isolated test runner + differential fuzzing
  complexity.py  empirical Big-O estimation
  srs.py         SM-2 scheduler          coach.py   practice suggestions
  stats.py       dashboard               scaffold.py / docs.py / cli.py
tests/           pytest suite
docs/PROBLEMS.md generated catalogue
```

MIT licensed.
