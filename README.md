# ACM Coach

Claude Code Skill for algorithm competition coaching. Designed for Codeforces, AtCoder, Luogu, ICPC and similar platforms.

[中文版](README.zh-CN.md)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude_Code_|_VS_Code-blue)](https://claude.ai/code)

## Features

| Scenario | Capability |
|----------|-----------|
| Stuck on a problem | Four-stage workflow (READ → THINK → CODE → VERIFY) — constraint analysis, algorithm selection, guided implementation |
| Getting WA / TLE / RE | Systematic diagnosis with line-level precision. Stress-test script included for counterexample discovery |
| Code needs review | Complexity audit, correctness check, edge case enumeration. Respects ACM conventions — no style nitpicking |
| Want to track progress | Automatic profiling across sessions — recurring bugs, strengths, weaknesses, CF-equivalent skill level |
| Have a solution folder | Batch reads your files, generates structured report: top mistakes, strengths, improvement priorities |
| Use Codeforces | Bind a CF handle — fetches rating history, analyzes topic-level AC rates, lists upcoming contests |
| Need a quick reference | 28 C++ algorithm templates (DSU, SegTree, Dijkstra, KMP, LCA, SCC, combinatorics) and 16 common pitfalls |

## Installation

Requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) (CLI or VS Code extension).

### Marketplace install

```bash
claude plugin marketplace add jojo-yin/acm-coach
claude plugin install acm-coach@acm-coach
```

### Git clone + project-level install

Keep the skill inside your own ACM practice folder — won't affect other projects.

```bash
# 1. Clone this repo anywhere (just for downloading)
git clone https://github.com/jojo-yin/acm-coach.git

# 2. Copy the skill into YOUR coding project
mkdir -p ~/my-acm-practice/.claude/skills
cp -r acm-coach/.claude/skills/acm-coach ~/my-acm-practice/.claude/skills/

# 3. Go to your project and start coding
cd ~/my-acm-practice
claude
```

Replace `~/my-acm-practice` with your actual ACM code directory. On Windows, use `%USERPROFILE%\my-acm-practice\.claude\skills\`.

### Git clone + user-level install

If you want the skill available globally (across all projects):

```bash
git clone https://github.com/jojo-yin/acm-coach.git
mkdir -p ~/.claude/skills
cp -r acm-coach/.claude/skills/acm-coach ~/.claude/skills/
```

To update: `git pull` in the cloned repo, then re-run the `cp -r` command above.

### Verify it works

Say something like "n=2e5, need O(n log n) at most, what algorithm should I use?" — if the agent analyzes the constraint before suggesting a solution, the skill is active.

## Usage

**Solving a problem from scratch:**

```
你: 这题完全没思路，n=2e5，求最大的子数组和不超过 k
Coach: 先看约束。n=2e5 → 复杂度预算 O(n log n)。子数组+最大值，想到什么数据结构？
你: 前缀和 + 二分？
Coach: 方向对了。但"不超过 k"意味着要找最小的前缀和差值...
```

**Debugging WA:**

```
你: WA 在第 3 个点了，帮我看看
    [贴代码]
Coach: 第 23 行：`for (int i=0; i<v.size()-1; i++)`
      当 v.size()=0 时，size()-1 = 18446744073709551615，死循环。
      改成 `i < (int)v.size() - 1`。
```

**Profile tracking (automatic, across sessions):**

```
（第 5 次 session）
你: review 一下这个 DP
Coach: 状态转移正确，复杂度 O(n²) 没问题。
      等等——第 15 行 `dp[i] = a[i] * b[i]`，两个 int 相乘。
      这已经是你第 4 次 int 溢出了，改 `1LL * a[i] * b[i]`。
```

The profile learns from every debugging and review session. A pattern must appear in 2+ sessions before it's confirmed, preventing one-off noise from becoming permanent. You can also explicitly tell it "记住，我喜欢迭代 DP 不要给我递归" and it will remember across sessions.

## What's Inside

```
.claude/skills/acm-coach/
├── SKILL.md              Core workflow and coaching rules (6 paths, 4 stages)
├── profile.md            Personal coding profile (gitignored, auto-updated)
├── references/
│   ├── algorithms.md     28 algorithm templates with complexity notes
│   ├── debugging.md      Systematic debugging workflow for WA/TLE/RE/MLE
│   ├── pitfalls.md       16 common C++ bugs with before/after examples
│   ├── teamwork.md       ICPC 3-person team strategy reference
│   └── cf-integration.md Codeforces API reference + rating rank ladder
└── scripts/
    ├── stress.py         Cross-platform stress test (in-memory, no temp files)
    └── cf_fetch.py       Codeforces API data fetcher (profile, rating, contests)
```

## Design

- **Coach, not a code generator.** Guides thinking, pinpoints bugs with minimal fixes. Won't output more than ~15 lines of code unless explicitly asked.
- **Token-efficient.** Progressive disclosure: only the description loads by default (~160 tokens). Reference files load on demand. The profile stays under ~200 tokens.
- **Respects ACM conventions.** Won't flag `#include <bits/stdc++.h>` or `using namespace std` as issues.

## Acknowledgments

Built with reference to [anthropics/skills](https://github.com/anthropics/skills), [OI Wiki](https://oi-wiki.org/), [CP-Algorithms](https://cp-algorithms.com/), [KACTL](https://github.com/kth-competitive-programming/kactl), [cc-habits](https://www.npmjs.com/package/cc-habits), and community experience from Codeforces, AtCoder, and Luogu. Full details in [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md).

## License

CC BY-SA 4.0.

## Changelog

### v0.2.1 (2026-07-05)

- **Help menu.** Asking "what can you do?" now shows a 6-path menu (A–F), no need to guess trigger phrases.
- **Features table.** Professionalized as a two-column `Scenario | Capability` layout, no emoji.
- **Changelog.** Release notes now tracked in README (EN + CN).

### v0.2.0 (2026-07-05)

- **D2: Automatic skill level assessment.** After every debug/review session, profile.md now tracks your CF-equivalent skill level using the Codeforces rank ladder (Newbie → Legendary Grandmaster).
- **Path F: Codeforces integration.** Bind a CF handle, fetch profile/rating history, get topic-level AC rate breakdown, and check upcoming contests — all via the public CF API.
- **`scripts/cf_fetch.py`.** Zero-dependency Python script for Codeforces API data fetching.
- **`references/cf-integration.md`.** CF API endpoint reference, rating rank ladder, and tag-to-topic mapping guide.
- **Fix:** Install guide rewritten — clone + copy to your own project directory, no longer locked to the acm-coach repo folder.
- **Fix:** Stress test script path unified across all reference files.

### v0.1.0 (2026-07-03)

Initial release.

- Four-stage problem-solving workflow (READ → THINK → CODE → VERIFY).
- Five coaching paths (Solve / Debug / Review / Profile / Team).
- 28 algorithm templates, 16 C++ pitfalls catalog, stress test script.
- Progressive disclosure: description ~160 tokens, references load on demand.
- User profiling with graduation gate, decay, and tombstones.

## License

CC BY-SA 4.0.

## Disclaimer

This is a personal side project, shared in the hope it helps fellow competitive programmers. It's not professionally maintained — expect rough edges, and don't rely on it as your only source of truth. Feedback and contributions are welcome.
