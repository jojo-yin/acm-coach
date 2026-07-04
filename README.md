# ACM Coach

Claude Code Skill for algorithm competition coaching. Designed for Codeforces, AtCoder, Luogu, ICPC and similar platforms.

[中文版](README.zh-CN.md)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude_Code_|_VS_Code-blue)](https://claude.ai/code)

## Features

- **Guided problem solving.** Four-stage workflow (READ-THINK-CODE-VERIFY) — doesn't dump code, leads with questions.
- **Systematic debugging.** Compile-reproduce first, then diagnose WA/TLE/RE/MLE with line-level precision. Minimal fixes only.
- **Code review.** Complexity check, correctness audit, edge case enumeration. No nitpicking on naming or style.
- **User profiling.** Tracks your recurring mistakes, strengths, and weaknesses across sessions. 2-session graduation gate prevents false patterns.
- **Batch analysis.** Reads your solution directory, generates a report: top mistakes, strengths, and improvement suggestions.
- **On-demand memory.** Say "remember this" and it writes to your profile, reminded in future sessions.
- **Algorithm templates.** 28 templates covering data structures, graph theory, number theory, DP, strings, geometry, and search.
- **C++ pitfalls catalog.** 16 common bugs with before/after examples, plus a diagnostic checklist.
- **Team contest reference.** ICPC 3-person-1-machine strategies, role division, and training plans.
- **Stress test script.** Cross-platform Python script, in-memory execution, zero temp files.

## Installation

Requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) (CLI or VS Code extension).

### Marketplace install

```bash
claude plugin marketplace add jojo-yin/acm-coach
claude plugin install acm-coach@acm-coach
```

### Git clone (VS Code)

```bash
git clone https://github.com/jojo-yin/acm-coach.git
cd acm-coach
code .
```

Open the Claude Code panel (`Ctrl+Shift+P` → `Claude Code: Open`). Skills in `.claude/skills/` load automatically.

### Git clone (Terminal)

```bash
git clone https://github.com/jojo-yin/acm-coach.git
cd acm-coach
claude
```

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
├── SKILL.md              Core workflow and coaching rules
├── profile.md            Personal coding profile (gitignored, auto-updated)
├── references/
│   ├── algorithms.md     28 algorithm templates with complexity notes
│   ├── debugging.md      Systematic debugging workflow for WA/TLE/RE/MLE
│   ├── pitfalls.md       16 common C++ bugs with before/after examples
│   └── teamwork.md       ICPC 3-person team strategy reference
└── scripts/
    └── stress.py         Cross-platform stress test (in-memory, no temp files)
```

## Design

- **Coach, not a code generator.** Guides thinking, pinpoints bugs with minimal fixes. Won't output more than ~15 lines of code unless explicitly asked.
- **Token-efficient.** Progressive disclosure: only the description loads by default (~160 tokens). Reference files load on demand. The profile stays under ~200 tokens.
- **Respects ACM conventions.** Won't flag `#include <bits/stdc++.h>` or `using namespace std` as issues.

## Acknowledgments

Built with reference to [anthropics/skills](https://github.com/anthropics/skills), [OI Wiki](https://oi-wiki.org/), [CP-Algorithms](https://cp-algorithms.com/), [KACTL](https://github.com/kth-competitive-programming/kactl), [cc-habits](https://www.npmjs.com/package/cc-habits), and community experience from Codeforces, AtCoder, and Luogu. Full details in [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md).

## License

CC BY-SA 4.0.

## Disclaimer

This is a personal side project, shared in the hope it helps fellow competitive programmers. It's not professionally maintained — expect rough edges, and don't rely on it as your only source of truth. Feedback and contributions are welcome.
