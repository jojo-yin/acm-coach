## Code Review: 0/1 Knapsack

### 1. Critical: Integer Overflow (Will Cause WA)

This is the most serious issue. The problem states `v[i] <= 10^9` and `n <= 100`. In the worst case, the total value sums to `100 * 10^9 = 10^11`, which far exceeds the range of a 32-bit `int` (max `2.147 * 10^9`). The `dp` array stores accumulated values, so once the sum crosses ~2.1 billion, it will overflow and produce wrong answers.

**Fix:** Change `dp` (and the internal value type) to `long long`:

```cpp
vector<vector<long long>> dp(n + 1, vector<long long>(W + 1, 0));
```

### 2. Memory: 2D DP May Be Wasteful

With `n = 100`, `W = 100,000`, a 2D `dp` array has `101 * 100001 ≈ 1.01 * 10^7` elements. If each element is a `long long` (8 bytes), that is about **80 MB**. Depending on the judge's memory limit (commonly 256 MB on modern platforms), this passes -- but it is borderline and unnecessary.

The standard optimization uses a **1D rolling array** (processing weights in reverse), which reduces memory to `O(W)`:

```cpp
vector<long long> dp(W + 1, 0);
for (int i = 0; i < n; i++) {
    for (int j = W; j >= w[i]; j--) {
        dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    }
}
```

### 3. Minor: Non-Standard Header

`#include <bits/stdc++.h>` is a GCC-specific internal header. While most competitive programming judges use GCC and accept it, it is not standard C++ and will fail on MSVC-based judges. If portability matters, replace it with the specific headers needed (`<iostream>`, `<vector>`, `<algorithm>`).

### 4. Minor: `using namespace std;` Typo

The line reads `using namespace std;` but it should be `using namespace std;`. Wait, let me re-examine -- actually, `using namespace std;` is the correct syntax. The code snippet shows exactly that, so this is fine. (I initially misread it.)

### 5. Trivial: Missing `return 0;`

While `main()` implicitly returns 0 in C++, some older judges or strict compilation flags may emit a warning. Adding `return 0;` at the end is a harmless best practice.

### Summary

| Severity | Issue | Impact |
|----------|-------|--------|
| **High** | `int` overflows for `v[i] <= 10^9` | Wrong Answer on large-value test cases |
| **Medium** | 2D DP uses ~80 MB memory | Potentially MLE on tight limits; waste of memory |
| **Low** | `bits/stdc++.h` non-portable | Compilation failure on non-GCC judges |
| **Trivial** | Missing `return 0;` | Warning at worst |

**Verdict:** The algorithm logic itself is correct -- it is the standard 0/1 knapsack DP. However, the `int` overflow bug means it will **not** reliably AC on the full test set. Fix the type to `long long` and consider the 1D space optimization for robustness.
