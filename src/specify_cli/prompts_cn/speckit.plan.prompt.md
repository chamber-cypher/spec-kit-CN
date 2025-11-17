---
description: 使用计划模板执行实现规划工作流程，生成设计工件。
---

## 用户输入

```text
$ARGUMENTS
```

你**必须**在继续之前考虑用户输入（如果不为空）。

## 概要

1. **设置**：从仓库根目录运行 `.specify/scripts/bash/setup-plan.sh --json`，并解析 JSON 以获取 FEATURE_SPEC、IMPL_PLAN、SPECS_DIR、BRANCH。对于 args 中的单引号如 "I'm Groot"，使用转义语法：例如 'I'\''m Groot'（或尽可能使用双引号："I'm Groot"）。

2. **加载上下文**：读取 FEATURE_SPEC 和 `.specify/memory/constitution.md`。加载 IMPL_PLAN 模板（已复制）。

3. **执行计划工作流程**：遵循 IMPL_PLAN 模板中的结构：
   - 填写技术上下文（将未知标记为"需要澄清"）
   - 从宪法填写宪法检查部分
   - 评估门控（如果违规未合理则为错误）
   - 阶段 0：生成 research.md（解决所有"需要澄清"）
   - 阶段 1：生成 data-model.md、contracts/、quickstart.md
   - 阶段 1：通过运行代理脚本更新代理上下文
   - 设计后重新评估宪法检查

4. **停止并报告**：阶段 2 规划后命令结束。报告分支、IMPL_PLAN 路径和生成的工件。