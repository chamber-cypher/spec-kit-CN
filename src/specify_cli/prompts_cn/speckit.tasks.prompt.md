---
description: 根据可用的设计工件，为功能生成一个可操作的、依赖关系排序的 tasks.md。
---

## 用户输入

```text
$ARGUMENTS
```

你**必须**在继续之前考虑用户输入（如果不为空）。

## 概要

1. **设置**：运行 `.specify/scripts/bash/setup-tasks.sh --json` 并解析 JSON 以获取 FEATURE_SPEC、TASKS_FILE、SPECS_DIR、BRANCH。

2. **加载上下文**：读取所有设计工件（FEATURE_SPEC、data-model.md、contracts/、quickstart.md 等）。

3. **生成任务工作流程**：
   - 分析所有可用的设计工件
   - 创建按依赖关系排序的任务列表
   - 确保每个任务都是可操作的
   - 包含必要的实现细节
   - 按优先级和依赖关系组织任务

4. **创建 tasks.md**：
   - 使用标准任务模板
   - 包含清晰的依赖关系说明
   - 提供足够的实现指导
   - 确保任务可跟踪和验证

5. **报告结果**：显示生成的 TASKS_FILE 路径和任务概要。