---
description: 在任务生成后对 spec.md、plan.md 和 tasks.md 执行非破坏性跨工件一致性和质量分析。
---

## 用户输入

```text
$ARGUMENTS
```

你**必须**在继续之前考虑用户输入（如果不为空）。

## 目标

在实施前识别三个核心工件（`spec.md`、`plan.md`、`tasks.md`）中的不一致性、重复、歧义和未明确说明的项目。此命令必须在 `/speckit.tasks` 成功生成完整的 `tasks.md` 后运行。

## 操作约束

**严格只读**：**不要**修改任何文件。输出结构化分析报告。提供可选的修复计划（用户必须明确批准，然后才能手动调用任何后续编辑命令）。

**宪法权威**：项目宪法（`.specify/memory/constitution.md`）在此分析范围内是**不可协商**的。宪法冲突自动为关键，需要调整规范、计划或任务 - 而不是稀释、重新解释或默默忽略原则。如果原则本身需要更改，那必须在 `/speckit.analyze` 之外的单独、明确的宪法更新中发生。

## 执行步骤

### 1. 初始化分析上下文

从仓库根目录**一次**运行 `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` 并解析 JSON 以获取 FEATURE_DIR 和 AVAILABLE_DOCS。派生绝对路径：

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md