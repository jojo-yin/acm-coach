# Algorithm Templates

Reference implementations for common ACM algorithms. All code follows a consistent style: `#include <bits/stdc++.h>`, `using namespace std`, `using ll = long long`, struct-wrapped where possible for multi-testcase safety.

## Contents

- [Complexity Budget](#complexity-budget)
- [Template Style](#template-style)
- [Data Structures](#data-structures) — DSU, Fenwick Tree
- [Graph Theory](#graph-theory) — Dijkstra, Floyd-Warshall, Topological Sort
- [Number Theory](#number-theory) — Fast Pow, GCD/LCM, Modular Inverse, Prime Sieve
- [Dynamic Programming](#dynamic-programming) — 0/1 Knapsack, LIS
- [String](#string) — KMP, Rolling Hash
- [More Data Structures](#more-data-structures) — Segment Tree (Lazy), Sparse Table, Trie
- [More Graph Theory](#more-graph-theory) — LCA (Binary Lifting), SCC (Tarjan)
- [More Number Theory](#more-number-theory) — Extended Euclidean, nCr mod Prime
- [Search & Optimization](#search--optimization) — Binary Search
- [Further Reading](#further-reading)

## Complexity Budget

| n range | Acceptable Complexity | Common Algorithms |
|---------|----------------------|-------------------|
| n ≤ 10 | O(n!), O(2^n) | Brute force, next_permutation |
| n ≤ 20 | O(2^n), O(n³) | Bitmask DP, Meet-in-Middle |
| n ≤ 100 | O(n³) | Floyd-Warshall, Interval DP |
| n ≤ 500 | O(n²) | Simple DP, Bubble-like |
| n ≤ 10^5 | O(n log n) | Sort + sweep, Dijkstra, SegTree, Fenwick |
| n ≤ 10^6 | O(n) | Linear scan, BFS, prefix sum, sieve |
| n ≤ 10^9 | O(log n), O(1) | Math, binary search, fast pow |

## Template Style

- Always `#include <bits/stdc++.h>` with `using namespace std` and `using ll = long long`
- Prefer `struct` over bare functions — easier to reset between testcases
- Use `1LL * a * b` for overflow-safe multiplication (portable, no GCC extensions)
- Arrays sized to `N = max_constraint + 5` for safety margin
- 1-indexed by default where it doesn't hurt readability

---

## Data Structures

### DSU (Disjoint Set Union)

Path compression + union by size. O(α(n)) amortized per operation.

```cpp
struct DSU {
    vector<int> fa, sz;
    DSU(int n) : fa(n + 1), sz(n + 1, 1) { iota(fa.begin(), fa.end(), 0); }
    int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }
    bool merge(int x, int y) {
        x = find(x), y = find(y);
        if (x == y) return false;
        if (sz[x] < sz[y]) swap(x, y);
        fa[y] = x; sz[x] += sz[y];
        return true;
    }
    bool same(int x, int y) { return find(x) == find(y); }
    int size(int x) { return sz[find(x)]; }
};
```

**Edge cases**: n=1 works (single element set). `find()` uses recursion — safe for n ≤ 2×10^5 but may overflow stack on long chains if path compression is omitted.

### Fenwick Tree (Binary Indexed Tree)

Point update, prefix sum query. O(log n) per operation. 1-indexed.

```cpp
struct Fenwick {
    int n; vector<ll> t;
    Fenwick(int n) : n(n), t(n + 1) {}
    void add(int i, ll x) { for (; i <= n; i += i & -i) t[i] += x; }
    ll sum(int i) { ll s = 0; for (; i > 0; i -= i & -i) s += t[i]; return s; }
    ll sum(int l, int r) { return sum(r) - sum(l - 1); }
};
```

**Common mistake**: Fenwick is 1-indexed. Passing i=0 causes an infinite loop (`i += i & -i` with i=0 is always 0).

---

## Graph Theory

### Dijkstra (Priority Queue)

O((V+E) log V). Assumes non-negative edge weights.

```cpp
struct Dijkstra {
    using Edge = pair<int, ll>; // to, weight
    int n; vector<vector<Edge>> g;
    Dijkstra(int n) : n(n), g(n + 1) {}
    void add(int u, int v, ll w) { g[u].push_back({v, w}); }

    vector<ll> run(int s) {
        vector<ll> d(n + 1, LLONG_MAX); d[s] = 0;
        priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
        pq.push({0, s});
        while (!pq.empty()) {
            auto [du, u] = pq.top(); pq.pop();
            if (du != d[u]) continue;
            for (auto [v, w] : g[u])
                if (d[v] > d[u] + w)
                    pq.push({d[v] = d[u] + w, v});
        }
        return d;
    }
};
```

**Key details**: `if (du != d[u]) continue` skips stale entries in the priority queue — essential for O(E log V). Without this line, the same node can be processed multiple times, degrading to O(VE) worst-case in dense graphs with repeated updates. Use `LLONG_MAX` not `1e18` — the latter is a `double` and causes precision issues when compared with `ll`.

### Floyd-Warshall (All-Pairs)

O(n³). Use only when n ≤ 500.

```cpp
// d[i][j] = initial edge weight or INF. After: d[i][j] = shortest path.
for (int k = 1; k <= n; k++)
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            if (d[i][k] < INF && d[k][j] < INF)
                d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
```

**Edge case**: Negative cycles: if `d[i][i] < 0` after the algorithm, a negative cycle exists along i's path. The `INF` check prevents overflow but won't detect unreachable nodes that get "updated" via INF.

### Topological Sort (Kahn's BFS)

O(V+E). Produces one valid ordering; returns empty vector if graph has a cycle.

```cpp
vector<int> topo(int n, const vector<vector<int>> &g) {
    vector<int> indeg(n + 1), res;
    for (int u = 1; u <= n; u++) for (int v : g[u]) indeg[v]++;
    queue<int> q;
    for (int u = 1; u <= n; u++) if (!indeg[u]) q.push(u);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        res.push_back(u);
        for (int v : g[u]) if (!--indeg[v]) q.push(v);
    }
    return (int)res.size() == n ? res : vector<int>();
}
```

---

## Number Theory

### Fast Pow (Modular Exponentiation)

O(log b). Compute `a^b mod m`. Overflow-safe using portable integer promotion — no `__int128` needed.

```cpp
ll binpow(ll a, ll b, ll m) {
    ll res = 1 % m; a %= m;
    while (b) {
        if (b & 1) res = res * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return res;
}
```

**Why this is safe**: `a` is reduced to `< m` before the loop. Each multiplication `a * a` produces a value `< m²`. For ACM, m is typically ≤ 10^9+7, so `m² ≈ 10^18` which fits in `long long` (max ≈ 9×10^18). If m can be up to 10^9, `m² = 10^18` still fits. Safe up to m ≤ 3×10^9.

**Edge case**: `m = 1` — `res = 1 % 1 = 0`, correct answer for any exponent.

### GCD / LCM

```cpp
ll gcd(ll a, ll b) { return b ? gcd(b, a % b) : a; }
ll lcm(ll a, ll b) { return a / gcd(a, b) * b; }
```

**Common mistake**: `lcm(a, b) = a * b / gcd(a, b)` overflows easily. Always divide first: `a / gcd(a, b) * b`.

### Modular Inverse (Fermat)

Requires m prime. `a^(m-2) mod m`.

```cpp
ll modinv(ll a, ll m) { return binpow(a, m - 2, m); }
```

### Prime Sieve (Eratosthenes)

O(n log log n). Generates primes up to n.

```cpp
vector<int> primes(int n) {
    vector<bool> is(n + 1, true); vector<int> p;
    for (int i = 2; i <= n; i++) {
        if (is[i]) p.push_back(i);
        for (int j : p) {
            if (1LL * i * j > n) break;  // overflow-safe
            is[i * j] = false;
            if (i % j == 0) break;       // linear sieve guarantee
        }
    }
    return p;
}
```

---

## Dynamic Programming

### 0/1 Knapsack

O(n×W). One-dimensional optimization.

```cpp
// items: vector of {weight, value}
// dp[j] = max value for capacity j
vector<ll> dp(W + 1);
for (auto [w, v] : items)
    for (int j = W; j >= w; j--)
        dp[j] = max(dp[j], dp[j - w] + v);
```

**Critical**: The inner loop goes **backwards** (j from W down to w). Going forward would allow reusing the same item multiple times (unbounded knapsack).

### LIS (Longest Increasing Subsequence)

O(n log n). Returns the length of LIS.

```cpp
int lis(const vector<int> &a) {
    vector<int> dp;
    for (int x : a) {
        auto it = lower_bound(dp.begin(), dp.end(), x);
        if (it == dp.end()) dp.push_back(x);
        else *it = x;
    }
    return (int)dp.size();
}
```

**Note**: `dp` does not contain the actual LIS — it's a helper array for computing the length. To reconstruct LIS, track parent indices separately.

**Strict vs non-strict**: `lower_bound` gives strictly increasing. Use `upper_bound` for non-decreasing (allows equal elements).

---

## String

Templates adapted from algorithm fundamentals. For deeper theory, see:
- [OI Wiki](https://oi-wiki.org/) (CC BY-SA 4.0 + SATA) — comprehensive Chinese-language algorithm reference
- [CP-Algorithms](https://cp-algorithms.com/) (CC BY-SA 4.0) — English-language algorithm encyclopedia
- [USACO Guide](https://usaco.guide/) — structured competitive programming curriculum

### KMP (Pattern Matching)

O(n+m). Returns all starting positions (0-indexed) of `pat` in `txt`.

```cpp
vector<int> kmp(const string &txt, const string &pat) {
    int n = txt.size(), m = pat.size();
    vector<int> pi(m), res;
    for (int i = 1, j = 0; i < m; i++) {
        while (j && pat[i] != pat[j]) j = pi[j - 1];
        if (pat[i] == pat[j]) pi[i] = ++j;
    }
    for (int i = 0, j = 0; i < n; i++) {
        while (j && txt[i] != pat[j]) j = pi[j - 1];
        if (txt[i] == pat[j] && ++j == m)
            res.push_back(i - m + 1), j = pi[j - 1];
    }
    return res;
}
```

### Rolling Hash (Double-Mod)

For substring hashing. Double-mod prevents collisions.

```cpp
struct Hash {
    static const ll M1 = 1e9 + 7, M2 = 1e9 + 9, B = 91138233;
    int n; vector<ll> h1, h2, p1, p2;
    Hash(const string &s) : n(s.size()), h1(n+1), h2(n+1), p1(n+1,1), p2(n+1,1) {
        for (int i = 0; i < n; i++) {
            h1[i+1] = (h1[i] * B + s[i]) % M1;
            h2[i+1] = (h2[i] * B + s[i]) % M2;
            p1[i+1] = p1[i] * B % M1;
            p2[i+1] = p2[i] * B % M2;
        }
    }
    pair<ll, ll> get(int l, int r) { // [l, r] 0-indexed
        ll v1 = (h1[r+1] - h1[l] * p1[r-l+1] % M1 + M1) % M1;
        ll v2 = (h2[r+1] - h2[l] * p2[r-l+1] % M2 + M2) % M2;
        return {v1, v2};
    }
};
```

---

## More Data Structures

### Segment Tree (Lazy Propagation)

Range add, range sum query. O(log n). Build in O(n). 1-indexed.

```cpp
struct SegTree {
    int n; vector<ll> t, lazy;
    SegTree(int n) : n(n), t(4*n), lazy(4*n) {}
    void build(int i, int l, int r, const vector<ll> &a) {
        if (l == r) { t[i] = a[l]; return; }
        int m = (l + r) / 2;
        build(i*2, l, m, a); build(i*2+1, m+1, r, a);
        t[i] = t[i*2] + t[i*2+1];
    }
    void push(int i, int l, int r) {
        if (!lazy[i]) return;
        int m = (l + r) / 2;
        t[i*2] += lazy[i] * (m - l + 1); lazy[i*2] += lazy[i];
        t[i*2+1] += lazy[i] * (r - m);   lazy[i*2+1] += lazy[i];
        lazy[i] = 0;
    }
    void add(int i, int l, int r, int ql, int qr, ll v) {
        if (ql <= l && r <= qr) { t[i] += v * (r - l + 1); lazy[i] += v; return; }
        push(i, l, r);
        int m = (l + r) / 2;
        if (ql <= m) add(i*2, l, m, ql, qr, v);
        if (qr > m)  add(i*2+1, m+1, r, ql, qr, v);
        t[i] = t[i*2] + t[i*2+1];
    }
    ll query(int i, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return t[i];
        push(i, l, r);
        int m = (l + r) / 2; ll s = 0;
        if (ql <= m) s += query(i*2, l, m, ql, qr);
        if (qr > m)  s += query(i*2+1, m+1, r, ql, qr);
        return s;
    }
};
```

**Common mistake**: Forgetting `push()` in `query()`. Lazy values must be propagated before descending, otherwise you read stale data. `4*n` array — segment tree has at most 4n nodes.

### Sparse Table (Static RMQ)

O(n log n) build, O(1) query. Immutable array only (no updates).

```cpp
struct SparseTable {
    vector<vector<int>> st;
    SparseTable(const vector<int> &a) {
        int n = a.size(), K = __lg(n) + 1;
        st.assign(K, vector<int>(n));
        for (int i = 0; i < n; i++) st[0][i] = a[i];
        for (int k = 1; k < K; k++)
            for (int i = 0; i + (1 << k) <= n; i++)
                st[k][i] = min(st[k-1][i], st[k-1][i + (1 << (k-1))]);
    }
    int query(int l, int r) { // [l, r] 0-indexed
        int k = __lg(r - l + 1);
        return min(st[k][l], st[k][r - (1 << k) + 1]);
    }
};
```

### Trie (Prefix Tree)

```cpp
struct Trie {
    struct Node { int cnt, end; int nxt[26]; Node() : cnt(0), end(0) { memset(nxt, 0, sizeof nxt); } };
    vector<Node> t;
    Trie() : t(1) {}
    void insert(const string &s) {
        int u = 0; t[u].cnt++;
        for (char c : s) {
            int &v = t[u].nxt[c - 'a'];
            if (!v) v = t.size(), t.emplace_back();
            u = v; t[u].cnt++;
        }
        t[u].end++;
    }
    int count(const string &s) { // exact match count
        int u = 0;
        for (char c : s) { u = t[u].nxt[c - 'a']; if (!u) return 0; }
        return t[u].end;
    }
    int prefix(const string &s) { // words with this prefix
        int u = 0;
        for (char c : s) { u = t[u].nxt[c - 'a']; if (!u) return 0; }
        return t[u].cnt;
    }
};
```

**Note**: Above uses lowercase a-z only. For larger alphabets, replace `nxt[26]` with `map<char, int>` at the cost of an extra log factor.

---

## More Graph Theory

### LCA — Binary Lifting

O(n log n) build, O(log n) query.

```cpp
struct LCA {
    int n, L; vector<vector<int>> g, up; vector<int> depth;
    LCA(int n) : n(n), g(n+1), depth(n+1) {
        L = __lg(n) + 1; up.assign(L, vector<int>(n+1));
    }
    void add(int u, int v) { g[u].push_back(v); g[v].push_back(u); }
    void dfs(int u, int p) {
        up[0][u] = p;
        for (int k = 1; k < L; k++) up[k][u] = up[k-1][up[k-1][u]];
        for (int v : g[u]) if (v != p) { depth[v] = depth[u] + 1; dfs(v, u); }
    }
    void build(int root = 1) { dfs(root, root); }
    int lca(int u, int v) {
        if (depth[u] < depth[v]) swap(u, v);
        int diff = depth[u] - depth[v];
        for (int k = 0; k < L; k++) if (diff >> k & 1) u = up[k][u];
        if (u == v) return u;
        for (int k = L - 1; k >= 0; k--)
            if (up[k][u] != up[k][v]) u = up[k][u], v = up[k][v];
        return up[0][u];
    }
};
```

### SCC — Tarjan

O(V+E). Returns SCC ID for each vertex (IDs in reverse topological order).

```cpp
struct Tarjan {
    int n; vector<vector<int>> g;
    vector<int> dfn, low, comp, stk; vector<bool> inStk;
    int timer = 0, scc_cnt = 0;
    Tarjan(int n) : n(n), g(n+1), dfn(n+1), low(n+1), comp(n+1), inStk(n+1) {}
    void add(int u, int v) { g[u].push_back(v); }
    void dfs(int u) {
        dfn[u] = low[u] = ++timer; stk.push_back(u); inStk[u] = true;
        for (int v : g[u]) {
            if (!dfn[v]) { dfs(v); low[u] = min(low[u], low[v]); }
            else if (inStk[v]) low[u] = min(low[u], dfn[v]);
        }
        if (dfn[u] == low[u]) {
            int v; ++scc_cnt;
            do { v = stk.back(); stk.pop_back(); inStk[v] = false; comp[v] = scc_cnt; } while (v != u);
        }
    }
    void run() { for (int i = 1; i <= n; i++) if (!dfn[i]) dfs(i); }
};
```

**Key**: SCC IDs decrease in topological order (higher ID = earlier in condensed DAG).

---

## More Number Theory

### Extended Euclidean + Modular Inverse (General Modulus)

Modular inverse when modulus is NOT prime (only needs gcd(a,m)=1).

```cpp
tuple<ll, ll, ll> exgcd(ll a, ll b) {
    if (!b) return {a, 1, 0};
    auto [g, x, y] = exgcd(b, a % b);
    return {g, y, x - a / b * y};
}
ll modinv_general(ll a, ll m) {
    auto [g, x, y] = exgcd(a, m);
    return g == 1 ? (x % m + m) % m : -1; // -1 = no inverse exists
}
```

### Combinatorics — nCr mod Prime

O(n) build, O(1) query. `mod` must be prime.

```cpp
struct Comb {
    int n; ll mod; vector<ll> fac, inv;
    Comb(int n, ll mod) : n(n), mod(mod), fac(n+1), inv(n+1) {
        fac[0] = 1;
        for (int i = 1; i <= n; i++) fac[i] = fac[i-1] * i % mod;
        inv[n] = binpow(fac[n], mod - 2, mod);
        for (int i = n; i > 0; i--) inv[i-1] = inv[i] * i % mod;
    }
    ll C(int n, int k) { return (k < 0 || k > n) ? 0 : fac[n] * inv[k] % mod * inv[n-k] % mod; }
};
```

---

## Search & Optimization

### Binary Search (Integer)

Find largest x where `check(x)` is true:

```cpp
ll lo = 0, hi = 1e18, ans = -1;
while (lo <= hi) {
    ll mid = lo + (hi - lo) / 2;
    if (check(mid)) ans = mid, lo = mid + 1;
    else hi = mid - 1;
}
```

For smallest x with `check(x)=true`: swap branches — `hi = mid - 1` in the true case.

### Floating-Point Binary Search

```cpp
double lo = 0, hi = 1e9;
for (int iter = 0; iter < 80; iter++) { // 80 iters → ~10^-24 precision
    double mid = (lo + hi) / 2;
    if (check(mid)) hi = mid; else lo = mid;
}
```

---

## Further Reading

All templates are adapted from well-established algorithm fundamentals. For theory, proofs, and advanced variants:

- **[OI Wiki](https://oi-wiki.org/)** (CC BY-SA 4.0 + SATA) — comprehensive Chinese-language algorithm reference
- **[CP-Algorithms](https://cp-algorithms.com/)** (CC BY-SA 4.0) — English-language algorithm encyclopedia
- **[USACO Guide](https://usaco.guide/)** — structured competitive programming curriculum
