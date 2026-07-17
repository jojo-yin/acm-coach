# Profile System Guide

Load this file only when Path D triggers (profile building, skill assessment, or memory requests).

Profile design adapted from [cc-habits](https://www.npmjs.com/package/cc-habits) (graduation gate, decay, tombstones), [OSS-Compass](https://oss-compass.org) (dual-dimension profiling), and [CF Analytics](https://cfanalytics.org) (topic-based weakness detection).

## Incremental Update (every Path B/C session)

Update **[profile.md](profile.md)** after each session. Rules:

**Graduation gate** (from cc-habits):
- First time seeing a pattern → put in `## Watching` (not yet active)
- Same pattern seen again in a later session → graduate to `## Active Bugs` / `## Active Strengths` / `## Active Weaknesses`

**Confidence & decay** (from cc-habits):
- Active patterns carry a count: `(N×, last: date)`. Increment N each time seen.
- If a pattern hasn't been seen in 5+ sessions, add `⚠️` to indicate it may be stale
- Stale patterns confirmed as no longer relevant → move to `## Tombstones`

**Tombstones** (from cc-habits):
- User explicitly says "I don't do that anymore" → move to `## Tombstones` with reason
- Tombstoned patterns are permanently blocked from re-appearing

**Topic Map** (from CF Analytics):
- Track problem-category performance with simple bars: `DP: ██░ | Graph: ███ | Greedy: █░░ | Math: ██░`
- Update based on what you observe in their code

**Token budget**: Entire profile.md must stay under ~200 tokens. Write in keyword shorthand. Only update if new. The `## Team` section is managed by Path E — don't touch it from Path D.

**At session start**: Quickly check profile.md. If current bug matches active pattern, mention it: "This is your 4th overflow bug — this is a recurring pattern for you."

## Batch Analysis (user explicitly triggers)

Trigger: "analyze my code" / "看看我的代码习惯" / "profile my solutions"

1. **Ask for directory** of their .cpp solution files
2. **Read all files** — for >20 files, sample newest 20 or span across topics
3. **Build profile** — recurring bugs (with file:line), strengths, weaknesses, style fingerprint, topic performance
4. **Present structured report** — top 3 mistakes (with evidence), top strengths, 2-3 highest-impact recommendations, topic map
5. **Populate profile.md** — batch results go directly in Active (batch counts as multi-session evidence)

**Token budget**: ≤2000 lines read. Use parallel reads. Report concise; detailed data lives in profile.md (≤50 lines).

## D2: Skill Level Assessment

Use the CF rank ladder as universal scale:

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

**If CF handle bound + data fresh (<7 days):** Use CF rating directly. Cross-reference with observed behavior — flag mismatches.

**If no CF handle:** Infer range from behavior. Key signals:
- Frequent overflow, off-by-one, brute-force only → Newbie–Pupil
- Algorithm usually correct, misses edge cases → Specialist–Expert
- Clean code, solid complexity awareness, rare bugs → Expert–CM+
Narrow range as data accumulates.

**If CF data stale (>7 days):** Fetch fresh: `python3 .claude/skills/acm-coach/scripts/cf_fetch.py profile <handle>`

**At session start:** Check `## Skill Level`. If current bug matches a known pattern, note it.

**Do NOT flag as problems:** `#include <bits/stdc++.h>`, `using namespace std`, brace style, indentation, naming conventions — these are standard CP practice.

## Memory on Demand

When user says "remember this" / "记住这个" / "don't forget" / "以后...":

- Write to `## Memory` in profile.md in keyword shorthand. Examples:
  - `"prefer: iterative DP over recursive"`
  - `"goal: reach 1800 rating by August"`
  - `"note: already studied CLRS graph chapters 22-25"`
- At future session starts, scan `## Memory`
- If Memory contradicts user's current direction, gently remind them
- Time-bound goals: if date passed, ask how it went
