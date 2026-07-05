# ACM Coach

面向算法竞赛的 Claude Code Skill。适用于 Codeforces、AtCoder、洛谷、ICPC 等平台。

[English](README.md)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude_Code_|_VS_Code-blue)](https://claude.ai/code)

## 功能介绍

- **引导解题。** 四阶段流程（READ-THINK-CODE-VERIFY），用问题引导思考，不直接给答案。
- **系统调试。** 先编译复现，再分类诊断 WA/TLE/RE/MLE，精准定位到行，只做最小改动。
- **代码审查。** 检查复杂度、正确性、边界情况。不揪命名风格和缩进。
- **用户画像。** 跨 session 追踪高频 bug、强弱项、编码习惯。2-session 毕业机制避免误报。
- **批量分析。** 通读题解目录，生成报告：高频错误、强项、改进建议。
- **手动记忆。** 说「记住这个」→ 写入画像，后续 session 自动提醒。
- **算法模板。** 28 个模板，覆盖数据结构、图论、数论、DP、字符串、几何、搜索。
- **C++ 陷阱。** 16 类常见错误，附修改前后对比和排查清单。
- **团队赛参考。** ICPC 三人一机策略、角色分工、训练体系。
- **对拍脚本。** 跨平台 Python 脚本，内存运行，无临时文件。

## 安装

需要先装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)（CLI 或 VS Code 扩展均可）。

### Marketplace 安装

```bash
claude plugin marketplace add jojo-yin/acm-coach
claude plugin install acm-coach@acm-coach
```

### Git clone + 项目级安装

把 skill 装在你自己的 ACM 刷题文件夹里，不会影响其他项目。

```bash
# 1. Clone 到任意位置（仅用于下载）
git clone https://github.com/jojo-yin/acm-coach.git

# 2. 把 skill 复制到你的刷题项目里
mkdir -p ~/my-acm-practice/.claude/skills
cp -r acm-coach/.claude/skills/acm-coach ~/my-acm-practice/.claude/skills/

# 3. 进入自己的项目开始写题
cd ~/my-acm-practice
claude
```

把 `~/my-acm-practice` 替换为你实际的 ACM 代码目录。Windows 用户用 `%USERPROFILE%\my-acm-practice\.claude\skills\`。

### Git clone + 用户级安装

如果想在所有项目中都能用这个 skill：

```bash
git clone https://github.com/jojo-yin/acm-coach.git
mkdir -p ~/.claude/skills
cp -r acm-coach/.claude/skills/acm-coach ~/.claude/skills/
```

更新方式：在 clone 的仓库中 `git pull`，然后重新执行上面的 `cp -r` 命令。

### 验证是否生效

随便说一句「n=2e5，应该用什么算法」，如果 agent 先分析复杂度预算再给建议，就说明加载成功了。

## 使用示例

**从零解题：**

```
你: 这题完全没思路，n=2e5，求最大的子数组和不超过 k
Coach: 先看约束。n=2e5 → 复杂度预算 O(n log n)。子数组+最大值，想到什么数据结构？
你: 前缀和 + 二分？
Coach: 方向对了。但"不超过 k"意味着要找最小的前缀和差值...
```

**调试 WA：**

```
你: WA 在第 3 个点了，帮我看看
    [贴代码]
Coach: 第 23 行：`for (int i=0; i<v.size()-1; i++)`
      当 v.size()=0 时，size()-1 = 18446744073709551615，死循环。
      改成 `i < (int)v.size() - 1`。
```

**跨 session 画像追踪：**

```
（第 5 次 session）
你: review 一下这个 DP
Coach: 状态转移正确，复杂度 O(n²) 没问题。
      等等——第 15 行 `dp[i] = a[i] * b[i]`，两个 int 相乘。
      这已经是你第 4 次 int 溢出了，改 `1LL * a[i] * b[i]`。
```

画像会在每次调试和审查后自动更新。同一个模式需要出现 2 次以上才会被确认，防止偶发误报。你也可以主动说「记住，我喜欢迭代 DP 不要给我递归」，它会在后续 session 中记住。

## 文件结构

```
.claude/skills/acm-coach/
├── SKILL.md              核心工作流和教练规则（6 个路径 + 4 个阶段）
├── profile.md            个人编码画像（gitignored，自动更新）
├── references/
│   ├── algorithms.md     28 个算法模板，附复杂度说明
│   ├── debugging.md      系统化调试流程（WA/TLE/RE/MLE）
│   ├── pitfalls.md       16 类 C++ 常见错误，附修改前后对比
│   ├── teamwork.md       ICPC 三人一机团队赛策略
│   └── cf-integration.md Codeforces API 参考 + rating 等级对照
└── scripts/
    ├── stress.py         对拍脚本（内存运行，无临时文件）
    └── cf_fetch.py       Codeforces API 数据获取（rating、比赛、提交记录）
```

## 设计原则

- **教练，不是代码生成器。** 引导思考，精准定位 bug，最小化修改。未经明确要求不输出超过约 15 行新代码。
- **Token 优先。** 渐进式加载：默认只加载 description（约 160 tokens），引用文件按需读取，画像控制在约 200 tokens 以内。
- **尊重 ACM 习惯。** 不会把 `#include <bits/stdc++.h>` 或 `using namespace std` 当作问题。

## 致谢

开发中参考了 [anthropics/skills](https://github.com/anthropics/skills)、[OI Wiki](https://oi-wiki.org/)、[CP-Algorithms](https://cp-algorithms.com/)、[KACTL](https://github.com/kth-competitive-programming/kactl)、[cc-habits](https://www.npmjs.com/package/cc-habits)，以及 Codeforces、AtCoder、洛谷等社区的经验分享。详见 [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md)。

## 更新日志

### v0.2.0 (2026-07-05)

- **D2：自动能力评估。** 每次 debug/review 后自动更新 profile.md，使用 Codeforces rank 体系评估水平等级（Newbie → Legendary Grandmaster）。
- **Path F：Codeforces 集成。** 绑定 CF 账号，获取 rating/rank/rating 走势，按 tag 统计 AC 率，查看即将开始的比赛——全部通过 CF 公开 API。
- **`scripts/cf_fetch.py`。** 零依赖 Python 脚本，统一调用 CF API。
- **`references/cf-integration.md`。** CF API 端点参考、rating 等级对照、tag 到知识点的映射指南。
- **修复：** 安装指引重写——从「clone 后锁死在 acm-coach 目录」改为复制到自己的项目文件夹中使用。
- **修复：** 对拍脚本路径在所有引用文件中统一。

### v0.1.0 (2026-07-03)

首次发布。

- 四阶段解题流程（READ → THINK → CODE → VERIFY）。
- 六个教练路径（解题 / 调试 / 审查 / 画像 / 团队 / CF）。
- 28 个算法模板、16 类 C++ 陷阱排查清单、对拍脚本。
- 渐进式加载：description 约 160 tokens，参考文件按需读取。
- 用户画像：毕业门机制 + 衰减 + 墓碑。

## 许可证

CC BY-SA 4.0。

## 免责声明

个人业余项目，顺手分享给同样打 ACM 的朋友。没有专业维护，可能有 bug，不要完全依赖它。欢迎提意见和 PR。
