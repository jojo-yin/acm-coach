# Codeforces Integration Guide

When Path F is triggered, load this file before responding. It covers: API usage, data interpretation, and how to map CF data to coaching insights.

## Data Fetching

Use the bundled script for structured output:

```bash
python3 .claude/skills/acm-coach/scripts/cf_fetch.py profile <handle>
python3 .claude/skills/acm-coach/scripts/cf_fetch.py rating <handle>
python3 .claude/skills/acm-coach/scripts/cf_fetch.py submissions <handle>
python3 .claude/skills/acm-coach/scripts/cf_fetch.py contests
```

The script handles rate limiting (1s between calls) and error formatting. If the script fails, fall back to `curl`:

```bash
curl -s "https://codeforces.com/api/user.info?handles=<handle>"
curl -s "https://codeforces.com/api/user.status?handle=<handle>&from=1&count=30"
curl -s "https://codeforces.com/api/contest.list?gym=false"
```

## CF API Endpoints

| Endpoint | Key Fields |
|----------|-----------|
| `user.info?handles={h}` | handle, rating, rank, maxRating, maxRank, registrationTimeSeconds, lastOnlineTimeSeconds, country, organization |
| `user.rating?handle={h}` | List of {contestName, rank, oldRating, newRating, ratingUpdateTimeSeconds} |
| `user.status?handle={h}&from=1&count=30` | List of {problem (with tags + rating), verdict, programmingLanguage, timeConsumedMillis} |
| `contest.list?gym=false` | List of {name, phase (BEFORE/FINISHED/CODING), startTimeSeconds, durationSeconds} |

## CF Rating Ranks

| Rank | Rating |
|------|--------|
| Newbie | < 1200 |
| Pupil | 1200–1399 |
| Specialist | 1400–1599 |
| Expert | 1600–1899 |
| Candidate Master | 1900–2099 |
| Master | 2100–2299 |
| International Master | 2300–2399 |
| Grandmaster | 2400–2599 |
| International Grandmaster | 2600–2999 |
| Legendary Grandmaster | ≥ 3000 |

## CF Problem Tags → ACM Topic Mapping

CF tags map to standard ACM categories. When analyzing a user's submissions, group tags:

| CF Tag | ACM Topic Area |
|--------|---------------|
| dp, greedy | 动态规划 / 贪心 |
| graphs, dfs and similar, bfs, shortest paths, trees, dsu | 图论 |
| data structures, binary search, sortings, two pointers | 数据结构 / 基础算法 |
| math, number theory, combinatorics, constructive algorithms | 数学 / 构造 |
| strings, string suffix structures | 字符串 |
| implementation, brute force | 模拟 / 暴力 |
| bitmasks, meet-in-the-middle | 状态压缩 / 搜索优化 |
| games, probabilities | 博弈 / 概率论 |
| flows, 2-sat | 网络流 / 高级图论 |
| geometry | 计算几何 |

## Analysis Output Template

When user triggers CF analysis:

1. **Profile**: "{handle} — rating {X} ({rank}), max {Y} ({maxRank}). Registered {date}."
2. **Trend**: "Last 5 contests: ↗/→/↘. Net change: ±Z. Best recent performance: {contest}."
3. **Topic strengths** (AC rate ≥ 60%): list top 3.
4. **Topic weaknesses** (AC rate ≤ 30%, or total ≥ 5 attempts + low AC): list top 3.
5. **Activity**: "N submissions in last month / recent window. Active/Very active/Inactive."
6. **Upcoming contests**: next 3–5, formatted as "Round #X — Date at Time (duration: Xh)".

## Edge Cases

- **Handle not found**: API returns "handle not found" → ask user to verify spelling
- **User unrated**: rating = 0, rank = "unrated" → note this, skip trend analysis
- **No recent submissions**: user.status returns [] → skip topic breakdown, note inactivity
- **CF API down/rate-limited**: retry once after 2s; if still failing, tell user to check later
- **Stale data**: if lastOnlineTimeSeconds is >3 months ago → flag as "inactive, data may be outdated"
- **Bound vs ad-hoc**: bound handle updates go to profile.md; ad-hoc lookups stay in conversation only

## Bound Handle Management

- **Set**: user says "bind CF <handle>" / 「绑定 CF 号 <handle>」 → write `bound: <handle>` to profile.md → `## Skill Level`
- **Clear**: user says "unbind CF" / 「解绑 CF」 → remove `bound:` line from profile.md
- **Use**: when user says "my CF" / 「我 CF」 without a specific handle → use bound handle
- The bound handle is also used for automatic rating refresh after Path B/C sessions
