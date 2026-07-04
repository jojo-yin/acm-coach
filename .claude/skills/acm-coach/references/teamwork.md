# ICPC Team Contest Strategy

Knowledge base for 3-person-1-machine team competitions. Sources: ICPC World Finals team post-mortems, [KACTL strategy doc](https://github.com/kth-competitive-programming/kactl), UT Austin ICPC research, and Chinese OI community team experiences.

## Three Classic Strategies

### 1. Simple Strategy (beginner teams)

Everyone reads problems independently. First to finish thinking codes. First to finish coding submits.

- ✅ Zero coordination overhead
- ❌ Multiple people finish easy problems simultaneously → machine queue forms after hour 1
- ❌ Hard problems never get reached
- **Verdict**: adequate for first contest; outgrow it quickly

### 2. Terminal Man (coder-specialist)

One designated "terminal man" owns the keyboard for the entire contest. The other two design algorithms on paper, write pseudocode, then hand written solutions to the terminal man to type.

- ✅ Eliminates machine bottleneck completely
- ✅ Clear separation: analysts focus on algorithms, coder focuses on typing
- ❌ Terminal man's algorithmic ability is wasted on pure transcription
- **Best when**: one teammate is significantly faster at typing + template recall

### 3. Think Tank (World Finals proven) 🏆

From the 1995 ICPC World Finals champion strategy, validated by multiple medal-winning teams since.

**First 15-30 minutes**: The two best analysts (the "Think Tank") jointly read and discuss **all problems**. The third person sets up templates and test harness during this time.

**By minute 15**: Think Tank picks the easiest problem for the coder to solve first.

**First hour**: Think Tank thoroughly discusses every problem, writing the core algorithm idea for each on paper.

**After hour 1**: Form a global judgment — decide *how many* problems the team aims to solve. Assign ownership of each.

**After 3.5 hours**: Stop writing new code. All remaining time is for debugging existing attempts.

> This strategy sacrifices early penalty time but solves **one more hard problem** than competitors — which is what wins ICPC.

## The Iron Triangle — Role Division

From multiple ICPC gold/silver medal teams:

| Role | Core Job | Key Trait |
|------|----------|-----------|
| **Thinker / Algorithm Lead** | Algorithm design, correctness proof, complexity analysis | Fast problem decomposition, constraint-to-algorithm mapping (e.g., n≤1e5 → O(n log n)) |
| **Coder / Implementer** | Transform algorithm into correct code, template mastery | 65%+ first-submit accuracy, can type without thinking about syntax |
| **Coordinator / Observer** | Read all problems, track progress, manage machine time, monitor team psychology | Global view, good at difficulty estimation, catches edge cases others miss |

**The complementarity rule**: No one is good at everything. Together, must cover: Data Structures, Graph Theory, DP, Math/Number Theory, Geometry, Strings.

**The hard truth** from experienced competitors: individual skill is the foundation. Coordination amplifies but doesn't replace it. "The team is only as strong as its strongest member." Focus on personal skill first, then team synergy.

## Contest Phases

### Opening (0-30 min)
- Fastest reader scans all problems, calls out estimated difficulties
- Identify the "sign-in" problem (solvable in 5-15 min) → coder executes immediately
- Get one AC on the board early — momentum matters

### Mid-contest (30 min — 3.5 h)
- Machine never idle — while one codes, others read new problems or prepare the next solution on paper
- Every problem read by at least 2 people before coding begins
- Track all problems in a **Problem Table**: read ✓, topic tag, difficulty estimate, status (attempted/AC/abandoned)
- If stuck on a problem for 15+ min → tag out, let fresh eyes drive
- Check scoreboard periodically: if a problem has many solves, it's easier than you think

### Last Hour (3.5 — 4.5 h)
- Stop starting new hard problems
- Switch to "free submit mode": getting one more AC matters more than penalty time
- All three focus on debugging existing attempts together

### Freeze Period (4 — 5 h)
- Scoreboard frozen but submissions still count
- Assume all other teams are still submitting — don't coast
- Prioritize the problem with highest confidence of AC

## Paper-First Debugging

The most universally agreed-upon rule from ICPC veterans:

> **"Real-time tracing is THE ULTIMATE SIN."**

- Do not debug by staring at the screen stepping through code
- Print the code and test output. Analyze on paper.
- The person at the keyboard codes; the other two debug on paper simultaneously
- After WA: re-read the problem statement word by word before touching the code

## Pre-Contest Preparation

### Team template
A shared `.cpp` skeleton all three members agree on: fast I/O, common macros, frequently used data structures. Everyone must be able to start coding from it without hesitation.

### Mock contests
At least 2 full 5-hour simulations with the actual 3-person-1-machine setup before a real contest. Practice handoffs: the coder steps away, someone else picks up the same file within 30 seconds.

### Post-contest retrospection
After every mock or real contest, do a **data-driven review**:
- How much time was spent reading vs coding vs debugging per problem?
- Classify errors: Algorithm wrong (30% typical) vs Implementation bug (50%) vs Misunderstood problem (20%)
- How many minutes was the machine idle? Why?
- Every mistake can only be made once

## Common Team Pitfalls

| Pitfall | Fix |
|---------|-----|
| Two people silently debugging the same code | Announce "I'm looking at line 23's loop bound" before starting |
| Coder implements wrong algorithm because Thinker was unclear | Thinker writes pseudocode on paper before coder types anything |
| All three tunnel-vision on one problem | Designate one person to always be reading new problems |
| "I'll fix this in 5 minutes" → 45 minutes later | 15-minute rule: stuck → tag out, no exceptions |
| Submitting without team review | All three must audibly agree before every submit |
| Obsessing over the scoreboard | Use as reference, not as a crutch. Top teams identify easy problems BEFORE they appear on the scoreboard |
| Assuming input format from samples | Never assume sorted, distinct, or bounded unless explicitly stated |

## Training System

| Phase | Duration | Focus |
|-------|----------|-------|
| Foundation | 1-2 months | Solo: topic-specific practice, 3-5 problems/day on one algorithm type |
| Reinforcement | 2-4 months | Mixed practice, 2-3 full 5-hour mock contests per week |
| Sprint | 1-2 months | Full-simulation mocks (same time, equipment, environment as real contest) |
| Taper | 2 weeks pre-contest | Psychological adjustment + tactical review, light practice only |

## References

- [KACTL Strategy Guide](https://github.com/kth-competitive-programming/kactl/blob/master/doc/strategy.pdf) — KTH Royal Institute of Technology's team strategy document
- ["Teamwork in Programming Contests: 3 × 1 = 4"](https://isaac.lsu.edu/class_2013_spring/local/3n.html) — LSU contest strategy reference
- ["破除个人英雄主义：ACM竞赛团队协同作战全解析"](https://developer.baidu.com/article/detail.html?id=6898319) — Baidu Developer article on ACM team coordination
- UT Austin ICPC research papers on team dynamics in programming contests
- Various ICPC World Finals team post-mortems and experience sharing from Chinese OI community (Zhihu, CSDN, Luogu)
