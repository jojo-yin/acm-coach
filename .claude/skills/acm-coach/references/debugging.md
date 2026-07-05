# Systematic Debugging for ACM

## Overview

Debugging is a skill, not luck. Randomly changing code and resubmitting is the slowest way to find a bug. This guide covers a repeatable process that works for every error type.

## Step 0: Reproduce Before Diagnosing

Before analyzing the code, confirm the failure is real and observe it directly:

```bash
g++ -std=c++17 -O2 -Wall -Wextra solution.cpp -o solution
./solution < sample_input.txt
```

Compiler warnings (`-Wall -Wextra`) often catch bugs before runtime. Do not skip them.

- Does the output differ from expected? → WA
- Does the program hang or exceed 1s for small input? → TLE
- Does it crash with a non-zero exit code? → RE
- Does the memory usage explode? → MLE

## Error Type Decision

```
What's the symptom?
    │
    ├─ Wrong output or wrong answer (WA)
    │       → Section: Debugging WA
    │
    ├─ Time Limit Exceeded (TLE)
    │       → Section: Debugging TLE
    │
    ├─ Runtime Error (RE) — crash, segfault, non-zero exit
    │       → Section: Debugging RE
    │
    └─ Memory Limit Exceeded (MLE)
            → Section: Debugging MLE
```

## Debugging WA (Wrong Answer)

WA means the program runs without crashing, but produces incorrect results. This is the most common and hardest to debug.

### Step 1: Re-read the problem

Before touching the code, re-read every word of the problem statement. The most common WA cause is a **misread constraint or requirement**:

- "lexicographically smallest" — did you output just any valid answer?
- "modulo 10^9+7" — did you forget the mod somewhere?
- "non-empty" / "positive" / "distinct" — did you handle these conditions?
- "at least" vs "exactly" — subtle preposition, completely different solution

### Step 2: Find a minimal counterexample

Instead of staring at the code, generate a failing test case. The smaller, the better:

**Method A — Binary search the bug location (for large inputs):**
If the code fails on a known large test, halve the input until the bug disappears, then expand. This isolates the exact data triggering the failure.

**Method B — Brute-force comparison (for small inputs):**
Write a correct-but-slow O(2^n) or O(n²) reference solution. Generate random small inputs (n ≤ 10). Use the bundled stress test script to compare them:

```bash
# 1. Compile all three
g++ -std=c++17 -O2 solution.cpp -o solution
g++ -std=c++17 -O2 brute.cpp -o brute
g++ -std=c++17 -O2 gen.cpp -o gen

# 2. Run stress test (cross-platform Python script)
python3 .claude/skills/acm-coach/scripts/stress.py --sol ./solution --brute ./brute --gen ./gen --limit 1000
```

Or use the bash one-liner (Linux/Mac only, auto-cleans temp files):
```bash
for i in $(seq 1 50); do
    ./gen > input.txt
    ./solution < input.txt > output.txt
    ./brute < input.txt > expected.txt
    if ! diff output.txt expected.txt; then
        echo "FAIL on test $i, input saved to fail_input.txt"
        mv input.txt fail_input.txt
        rm -f output.txt expected.txt
        break
    fi
    rm -f input.txt output.txt expected.txt
done
```

The script automatically saves the first diverging input to `fail_input.txt` — open it, it's small enough to trace by hand.

**Method C — Edge case enumeration:**
If brute-force isn't feasible, manually construct and test these universal edge cases:

- n = 1 (minimum input)
- n = max constraint value
- All values equal (e.g., all zeros, all ones)
- Strictly increasing / decreasing sequence
- Alternating pattern
- Values that cause overflow (10^9 × 10^9)

### Step 3: Trace with the counterexample

Once you have a small failing input, trace the code line by line with that input. Write down variable values at each step. The moment reality diverges from expectation — that's your bug.

### Step 4: Verify the fix

After fixing, compile and rerun:
1. The failing counterexample — must now pass
2. All sample testcases — must still pass
3. The original large test case — must now pass
4. Your edge case suite — must all pass

## Debugging TLE (Time Limit Exceeded)

TLE means the algorithm is too slow. The fix is usually algorithmic, not micro-optimization.

### Step 1: Calculate the actual complexity

What is the real worst-case number of operations? Multiply:
- Number of testcases × iterations per case × operations per iteration
- Must stay under ~10^8 for a 1s limit in C++

### Step 2: Find hidden inner loops

These patterns look O(n) but are actually O(n²):

| Pattern | Why It's O(n²) |
|---------|---------------|
| `v.erase(it)` inside a loop | `erase()` shifts all subsequent elements — O(n) each |
| `s = s + c` in a loop | String concatenation creates a new string each time |
| `find()` on `vector` or `set` where `map` would work | O(n) lookup inside an O(n) loop |
| `unordered_map` with many collisions | Worst-case O(n) per operation |
| Recursion with overlapping subproblems, no memoization | Recomputation explosion |

### Step 3: Algorithmic fixes (in order of priority)

1. **Change the algorithm** — O(n²) to O(n log n) usually means replacing brute-force with sort + sweep, or nested loops with prefix sums / two pointers
2. **Add memoization** — cache results of expensive recursive calls
3. **Replace container** — `map` → `unordered_map`, `set` → `vector` + `sort` + `unique`, `list` → `vector`
4. **Constant micro-optimizations** (only when you're close to the limit):
   - `'\n'` instead of `endl`
   - `ios::sync_with_stdio(false); cin.tie(nullptr);`
   - `vector::reserve()` when size is known
   - Pass large objects by `const &` instead of by value

## Debugging RE (Runtime Error)

RE means the program crashed. Common causes:

### Segfault / Access Violation

1. **Array index out of bounds** — most common. Check all `arr[i]` accesses against array size. Common off-by-one: `for (i=0; i<=n; i++)` on a size-n array
2. **Recursion depth exceeded** — stack overflow from deep recursion (e.g., DFS on a chain of 10^5 nodes). Fix: rewrite as iteration, or increase stack size: `ulimit -s unlimited` (local), `-Wl,--stack,268435456` (MinGW/Windows)
3. **Negative array index** — `arr[-1]` or `dp[-1]`. Check all index expressions
4. **Dereferencing null/erased iterator** — `*it` after `erase(it)`. Use `it = erase(it)` pattern

### Division by Zero

Check every `/` and `%` operator — is the denominator ever zero?

### Using `gdb` for RE

```bash
g++ -g -std=c++17 solution.cpp -o solution
gdb ./solution
(gdb) run < input.txt
# When it crashes, gdb shows the exact line
(gdb) bt  # backtrace — shows call stack
```

## Debugging MLE (Memory Limit Exceeded)

1. **Check array sizes** — `int arr[10^8]` ≈ 400MB, exceeds 256MB limit. Use `vector` with exact sizing
2. **Recursion with large local variables** — each stack frame carries copies of local arrays. Move large locals to heap or global scope
3. **STL containers growing unbounded** — `vector::push_back` in an infinite or unexpectedly large loop
4. **Memory leak (rare in competitive programming)** — `new` without `delete`, but STL containers handle cleanup automatically

## Quick Reference: Common Bug Checklist

When you don't know where to start, run through this list:

- [ ] `int` overflow — any multiplication of values ≥ 10^5?
- [ ] `long long` used everywhere it's needed?
- [ ] Off-by-one — ≤ vs <, 0-index vs 1-index?
- [ ] Multi-testcase — all globals reset in `solve()`?
- [ ] `memset` for non-zero/non-minus-one values? (only 0 and -1 work per byte)
- [ ] `1 << k` where k ≥ 31? (use `1LL << k`)
- [ ] Modulo applied to ALL growing values?
- [ ] `endl` used in output-heavy code? (use `'\n'`)
- [ ] Array size ≥ constraint maximum + buffer?
- [ ] Edge case n=1 handled?
- [ ] Edge case n=max handled?
- [ ] Floating point equality without epsilon?
- [ ] `size()` compared with `int` (signed/unsigned mismatch)?
- [ ] Iterator invalidation after `push_back` / `erase`?

## When to Give Up and Ask for Help

After systematically working through the checklist above, if you still can't find the bug:

1. Share the **problem link** so the coach can read the original statement
2. Share the **failing code** (not a description — the actual file)
3. Describe what you've already tried — this prevents the coach from suggesting things you've ruled out
4. If you have a **failing test case**, share that too — it's the fastest way to reproduce
