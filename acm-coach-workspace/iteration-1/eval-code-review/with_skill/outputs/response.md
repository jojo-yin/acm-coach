## Path C: Code Review -- 0/1 Knapsack

### 1. Complexity Check

| Metric | Value | Assessment |
|--------|-------|------------|
| Time | O(n * W) = 100 * 10^5 = **10^7** | Fine for 1s |
| Space (current, `int`) | (n+1)*(W+1)*4 bytes = **~40 MB** | OK for 256 MB |
| Space (if `long long`) | (n+1)*(W+1)*8 bytes = **~80 MB** | Still OK for 256 MB, but getting heavy |

The algorithm itself is the correct complexity class for these constraints.

### 2. Correctness

The DP logic is standard and correct:
- **State definition**: `dp[i][j]` = max value using first `i` items with weight limit `j` -- correct.
- **Transition**: `dp[i][j] = max(dp[i-1][j], dp[i-1][j - w[i-1]] + v[i-1])` -- correct 0/1 knapsack recurrence.
- **Base case**: `dp[0][*] = 0` -- correct.
- **Answer**: `dp[n][W]` -- correct.

### 3. Edge Case Audit

| Edge Case | Behavior | Verdict |
|-----------|----------|---------|
| W = 0 | dp[*][0] = 0, loop body skipped when j >= w[i-1] is false | OK |
| n = 1 | Single-item DP works correctly | OK |
| All items too heavy (w[i] > W) | dp stays 0 | OK |
| All w[i] = 0 | j >= 0 always true, items always taken | OK |

### 4. Critical Issue: Integer Overflow

This is the one real bug. `v[i] <= 10^9`, and with `n <= 100`, the maximum total value is:

```
100 * 10^9 = 10^11
```

But `int` (32-bit signed) maxes out at **2,147,483,647** (~2.1 * 10^9). That means **any test case where the answer exceeds ~2 billion will silently overflow** and produce a wrong answer. With v[i] up to 10^9, just 3 items with v = 10^9 already overflow.

**Line 9:**
```cpp
vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
```

The `int` in `dp` is the problem. It needs to be `long long`. Also change `v` to `vector<long long>` for consistency (though individual values fit in int, the sum across rows does not).

**Minimal fix:** Change the dp type:
```cpp
vector<vector<long long>> dp(n + 1, vector<long long>(W + 1, 0));
```

And `vector<long long> v(n)` to match.

### 5. Space Optimization Opportunity (Not a Bug)

This is the classic 2D DP for 0/1 knapsack -- it works, but you only ever read from row `i-1`. You can reduce it to a 1D array and iterate `j` backwards:

```cpp
vector<long long> dp(W + 1, 0);
for (int i = 0; i < n; i++)
    for (int j = W; j >= w[i]; j--)
        dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
```

This cuts space from O(n*W) to O(W). For your constraints it is not strictly necessary (~80 MB still fits in 256 MB), but it is the idiomatic competitive programming version and guards against tighter memory limits.

### 6. Verdict

| Category | Grade | Note |
|----------|-------|------|
| Algorithm choice | Correct | 0/1 knapsack DP, O(n*W) fits constraints |
| DP logic | Correct | Standard recurrence, correct transitions |
| Edge cases | Covered | Handles W=0, n=1, all-heavy items |
| Data types | **Bug** | `int` overflows at ~2*10^9; answer can reach 10^11 |
| Space | Adequate | 2D is fine here, 1D would be better practice |

**Summary:** The algorithm is solid. The single issue is a **data type overflow**: `int` cannot hold the answer when v[i] are large. Change `dp` (and `v`) to `long long`. The answer will be wrong on any non-trivial test case otherwise.
