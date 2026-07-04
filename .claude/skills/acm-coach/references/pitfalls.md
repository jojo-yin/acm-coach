# C++ Competition Pitfalls

A catalog of the most common bugs in competitive programming C++ code. Each entry includes what goes wrong, why, and the fix. Organized by how often they appear in real contests.

## Integer Overflow

**The #1 most common ACM bug.** Silent, no compiler warning, and your code looks correct.

### Multiplication before assignment

```cpp
// ❌ BAD: a and b are int, multiplication happens in int, THEN assigned to ll
int a = 100000, b = 100000;
long long ans = a * b;  // a*b = 10^10 → wraps to ~1.4×10^9 in int

// ✅ GOOD: promote to long long before multiplication
long long ans = 1LL * a * b;
```

### Accumulation overflow

```cpp
// ❌ BAD: sum is int, overflows silently when total exceeds 2×10^9
int sum = 0;
for (int x : arr) sum += x;

// ✅ GOOD
long long sum = 0;
```

### Loop bound overflow

```cpp
// ❌ BAD: i*i computed in int; when i > 46340, i*i overflows to negative
for (int i = 2; i * i <= n; i++)

// ✅ GOOD: cast to ll before multiplication
for (long long i = 2; i * i <= n; i++)
```

**Rule of thumb**: If any value can exceed 2×10^9, use `long long`. In ACM, this means almost always.

## Bitshift Overflow

```cpp
// ❌ BAD: 1 is int, shifted left 40 times → undefined behavior
long long mask = 1 << 40;

// ✅ GOOD
long long mask = 1LL << 40;
```

`1 << k` is `int << int = int`. When k ≥ 31, the result overflows or is undefined. Use `1LL` to make the literal `long long`.

## Modulo Mistakes

### Forgetting mod on intermediate results

```cpp
// ❌ BAD: intermediate can overflow before mod
ll ans = (a * b) % MOD;  // a*b may overflow ll if a,b ≥ 10^9

// ✅ GOOD: mod after each multiplication
ll ans = a * b % MOD;    // safe when a,b < MOD (common case)
// Or for mod near 10^9:
ll ans = (__int128)a * b % MOD;
```

### Negative modulo

```cpp
// ❌ BAD: in C++, -1 % MOD = -1 (not MOD-1)
ll x = (a - b) % MOD;

// ✅ GOOD: ensure non-negative
ll x = ((a - b) % MOD + MOD) % MOD;
```

## `memset` Misuse

`memset` works **byte by byte**, not element by element. It only produces correct results for 0 and -1 (all bits zero or all bits one).

```cpp
// ❌ BAD: sets each BYTE to 1, so int becomes 0x01010101 ≈ 16 million
int dp[100];
memset(dp, 1, sizeof(dp));

// ✅ GOOD: use fill or std::fill
fill(dp, dp + 100, 1);
```

```cpp
// ✅ OK: memset with 0 and -1 works correctly
memset(dp, 0, sizeof(dp));   // all bits zero → int = 0
memset(dp, -1, sizeof(dp));  // all bits one  → int = -1 (two's complement)
```

## Multi-Testcase Cleanup

Global or static variables persist between testcases. Forgetting to reset them is the most common cause of "passes first case, fails rest."

```cpp
// ❌ BAD: global arrays retain data from previous testcase
vector<int> adj[N];
bool vis[N];

void solve() {
    int n, m; cin >> n >> m;
    // adj[i] still has edges from last testcase!
    // vis[i] still true from last testcase!
}

// ✅ GOOD: clear at start of each solve()
void solve() {
    int n, m; cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        adj[i].clear();
        vis[i] = false;
    }
}

// ✅ ALSO GOOD: use struct-wrapped containers that go out of scope
void solve() {
    int n, m; cin >> n >> m;
    vector<vector<int>> adj(n + 1);  // fresh each call
    vector<bool> vis(n + 1);
}
```

**Checklist for multi-testcase**: global arrays, `vector` (if not re-declared), `set/map` contents, static variables inside functions, `fill`/`memset` calls.

## Floating Point Precision

```cpp
// ❌ BAD: direct equality on floating point
double a = 0.1 + 0.2;
if (a == 0.3) ...  // FALSE! 0.1+0.2 = 0.30000000000000004

// ✅ GOOD: epsilon comparison
const double EPS = 1e-9;
if (fabs(a - b) < EPS) ...     // a == b
if (a < b - EPS) ...           // a < b
if (a < b + EPS) ...           // a ≤ b
```

**Rule**: never use `==`, `!=`, `<`, `>` on `double`/`float` without an epsilon. Use `int`/`long long` for all comparisons whenever possible (e.g., compare squared distances instead of square roots).

## STL Iterator Invalidation

### Erasing while iterating

```cpp
// ❌ BAD: it becomes invalid after erase()
for (auto it = v.begin(); it != v.end(); ++it)
    if (*it % 2 == 0) v.erase(it);  // CRASH

// ✅ GOOD: use returned iterator
for (auto it = v.begin(); it != v.end(); )
    if (*it % 2 == 0) it = v.erase(it);
    else ++it;
```

### push_back on vector

```cpp
// ❌ BAD: push_back may reallocate, invalidating all iterators
vector<int> v = {1, 2, 3};
for (auto it = v.begin(); it != v.end(); ++it)
    if (*it == 2) v.push_back(4);  // it may be invalid now

// ✅ GOOD: collect additions, apply after loop, or use reserve()
v.reserve(v.size() + count_additions);
```

## `endl` vs `\n`

```cpp
// ❌ BAD: endl flushes output buffer every time — hundreds of ms wasted
for (int i = 0; i < 1000000; i++)
    cout << i << endl;

// ✅ GOOD: \n doesn't flush; buffer flushes once at the end
for (int i = 0; i < 1000000; i++)
    cout << i << '\n';
```

`endl` = `'\n'` + `flush()`. Flushing 10^6 times can turn a 0.1s output into 2s → TLE. Use `endl` only when you need the output to appear immediately (interactive problems).

## `size()` Signed/Unsigned Mismatch

```cpp
// ❌ BAD: v.size() is size_t (unsigned), compared with int
vector<int> v;
for (int i = 0; i < v.size() - 1; i++)  // if size=0, size()-1 = SIZE_MAX → infinite loop!

// ✅ GOOD: cast to int
for (int i = 0; i < (int)v.size() - 1; i++)

// ✅ ALSO GOOD: use size_t (but be careful with backwards loops)
for (size_t i = 0; i + 1 < v.size(); i++)
```

The `v.size() - 1` when `v.size() == 0` is the classic trap: `0u - 1u = 18446744073709551615` (SIZE_MAX).

## Stack Overflow from Recursion

DFS on a chain of 10^5 nodes → recursion depth 10^5 → stack overflow.

```cpp
// ❌ BAD: recursive DFS on large linear structure
void dfs(int u) {
    for (int v : g[u]) dfs(v);
}

// ✅ FIX 1: increase stack size (platform-dependent)
// Linux: ulimit -s unlimited
// Windows/MinGW: -Wl,--stack,268435456 (256MB)

// ✅ FIX 2: rewrite as iteration with explicit stack
void dfs_iterative(int start) {
    vector<int> stk = {start};
    while (!stk.empty()) {
        int u = stk.back(); stk.pop_back();
        // process u, push children
    }
}
```

## `unordered_map` Hash Collision

`unordered_map` uses a fixed hash function that can be hacked in Codeforces (anti-hash tests).

```cpp
// ❌ RISKY: O(n) per operation on crafted anti-hash inputs
unordered_map<int, int> cnt;

// ✅ SAFE: O(log n) guaranteed, usually fast enough
map<int, int> cnt;

// ✅ ALSO SAFE: custom hash for unordered_map
#include <chrono>
struct custom_hash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15; x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
        x = (x ^ (x >> 27)) * 0x94d049bb133111eb; return x ^ (x >> 31);
    }
    size_t operator()(uint64_t x) const {
        static const uint64_t FIXED_RANDOM = chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(x + FIXED_RANDOM);
    }
};
unordered_map<int, int, custom_hash> cnt;
```

## `lower_bound` on Set

```cpp
// ❌ BAD: O(n) for set — std::lower_bound doesn't know about tree structure
auto it = lower_bound(s.begin(), s.end(), x);

// ✅ GOOD: O(log n) — member function uses the tree
auto it = s.lower_bound(x);
```

## Fast I/O

```cpp
// Always at the start of main():
ios::sync_with_stdio(false);
cin.tie(nullptr);
```

Without this, `cin` is synchronized with C's `stdio`, making it ~10× slower. Also, never mix `cin`/`cout` with `scanf`/`printf` after this.

## Off-by-One with 0-index vs 1-index

```cpp
// ❌ BAD: mixing conventions — graph is 1-indexed but loop goes 0..n-1
vector<int> adj[N];
for (int i = 0; i < n; i++) dfs(i);  // never visits node n

// ✅ GOOD: be explicit and consistent
for (int i = 1; i <= n; i++) dfs(i);
```

## Passing Large Objects by Value

```cpp
// ❌ BAD: copies entire vector on every call → O(n) per call = O(n²) total
void dfs(int u, vector<int> path) { ... }

// ✅ GOOD: pass by reference (const if read-only)
void dfs(int u, vector<int> &path) { ... }
void dfs(int u, const vector<int> &path) { ... }
```

## Quick Diagnostic Checklist

When debugging, run through this list before deep-diving:

1. `int` where `long long` needed? Check every multiplication and sum.
2. `1 << k` vs `1LL << k`? Check every shift.
3. Multi-testcase cleanup? Check every global array and static variable.
4. `memset` with values other than 0 or -1? Replace with `fill`.
5. `size()` compared with `int`? Cast or use `size_t`.
6. `endl` in loops? Replace with `'\n'`.
7. Modulus applied everywhere? Check negative results too.
8. `unordered_map` without custom hash? Consider `map`.
9. Iterator invalidation in `erase`/`push_back` loops?
10. Pass-by-value for large containers? Use `const &`.

## Interactive Problems

Codeforces/AtCoder increasingly uses interactive problems where your program communicates with a judge.

### Flush after every output

The #1 interactive bug: forgetting to flush. The judge never sees your query, both programs hang → Idleness Limit Exceeded.

```cpp
// ❌ BAD: no flush — judge never receives this query
cout << "? 1 5\n";

// ✅ GOOD: endl auto-flushes
cout << "? 1 5" << endl;

// ✅ ALSO GOOD: manual flush after \n
cout << "? 1 5\n" << flush;
```

### cin.tie(0) breaks automatic flushing

Normally `cin >> x` auto-flushes `cout`. But after `cin.tie(nullptr)`, this tie is broken:

```cpp
ios::sync_with_stdio(false);
cin.tie(nullptr);  // breaks cin-cout tie!

// In interactive problems, must now manually flush EVERY output:
cout << "? 1 5" << endl;  // endl = \n + flush
int response; cin >> response;
```

**Rule**: In interactive problems, either (a) don't use `cin.tie(0)`, or (b) always use `endl`/`flush`.

### #define endl "\n" kills interactive

Many ACM templates do `#define endl '\n'` for speed. In interactive problems, this removes the flush behavior of `endl`:

```cpp
#define endl '\n'  // ❌ DO NOT USE IN INTERACTIVE PROBLEMS
```

Remove this macro or replace `endl` with explicit `cout.flush()` calls.

### Final answer must also be flushed

```cpp
cout << "! " << answer << endl;  // flush the answer too
```

