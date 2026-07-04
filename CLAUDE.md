# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

本项目旨在创建一个面向 **ACM 算法竞赛**的 Claude 通用 Skill。该 Skill 将为参赛者提供算法辅导、代码审查、调试辅助、时间复杂度分析、反例构造等能力。

最终交付物是 `.claude/skills/acm-coach/SKILL.md` 及其配套参考文件。

## 核心开发原则

**REQUIRED BACKGROUND:** 编写 Skill 必须使用 `superpowers:writing-skills` 中的 TDD 方法论——**没有失败的测试之前，不写任何 Skill 内容**。

Skill 开发的铁律：
1. RED: 先用 subagent 运行 baseline 场景（不用 skill），记录 agent 的原始行为和错误
2. GREEN: 针对 baseline 中的具体问题，写最少的内容解决它们
3. REFACTOR: 发现新的漏洞 → 精准修补 → 重新验证

**不要做的：**
- 批量创建多个 skill 而不逐一测试
- 在没见过 agent 失败之前就写内容
- 写多语言示例（一个优秀的示例就够了）
- 在 description 中总结工作流程（只写触发条件）

## Skill 目录结构

```
.claude/skills/acm-coach/
├── SKILL.md              # 主 Skill 文件（必需）
├── references/           # 参考文件（按需加载）
│   ├── algorithms.md     # 算法模板与复杂度速查
│   ├── debugging.md      # ACM 调试技巧
│   └── pitfalls.md       # 常见陷阱
└── scripts/              # 工具脚本（按需执行）
```

## SKILL.md 格式要求

- YAML frontmatter 必须包含 `name`（字母/数字/连字符，64 字符以内）和 `description`（使用场景，1024 字符以内）
- `description` 以 "Use when..." 开头，用第三人称，只描述触发条件，不总结内部流程
- SKILL.md 正文控制在 500 行以内，大型参考内容拆分到独立文件
- 渐进式加载：主体放 SKILL.md，附加放 references/，脚本放 scripts/

## 项目中的文件

- `.claude/settings.local.json` — 项目本地配置（安装了 superpowers@claude-plugins-official, scope: local）
- `test.cpp` — 用于测试 Skill 效果的 ACM 风格 C++ 代码示例
- `.exe` — 编译产物，应加入 `.gitignore`

## 工具链

- 语言偏好：ACM 竞赛常用 C++（g++），Python 用于辅助脚本
- Skill 测试：使用 `Skill` 工具在真实 ACM 题目上验证 Skill 效果
- 编写 Skill 时调用 `Skill` 工具触发 `superpowers:writing-skills` 获取完整开发指导
