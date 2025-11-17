---
description: 通过自然语言功能描述创建或更新功能规范。
---

## 用户输入

```text
$ARGUMENTS
```

你**必须**在继续之前考虑用户输入（如果不为空）。

## 概要

用户在触发消息中在 `/speckit.specify` 之后输入的文本**就是**功能描述。假设即使 `$ARGUMENTS` 在字面上显示在下面，你始终可以在此对话中使用它。除非用户提供了空命令，否则不要要求用户重复它。

根据该功能描述，执行以下操作：

1. **为分支生成一个简洁的短名称**（2-4个词）：
   - 分析功能描述并提取最有意义的关键词
   - 创建一个2-4个词的短名称，抓住功能的核心
   - 尽可能使用动作-名词格式（例如，"add-user-auth", "fix-payment-bug"）
   - 保留技术术语和缩写词（OAuth2, API, JWT等）
   - 保持简洁但具有足够的描述性，以便一目了然地理解功能
   - 示例：
     - "I want to add user authentication" → "user-auth"
     - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
     - "Create a dashboard for analytics" → "analytics-dashboard"
     - "Fix payment processing timeout bug" → "fix-payment-timeout"

2. **在创建新分支之前检查现有分支**：

   a. 首先，获取所有远程分支以确保我们有最新信息：
      ```bash
      git fetch --all --prune
      ```

   b. 从所有来源中找到短名称的最高功能编号：
      - 远程分支：`git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
      - 本地分支：`git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
      - 规范目录：检查匹配 `specs/[0-9]+-<short-name>` 的目录

   c. 确定下一个可用编号：
      - 从所有三个来源中提取所有数字
      - 找到最高编号 N
      - 对新分支编号使用 N+1

   d. 运行脚本 `.specify/scripts/bash/create-new-feature.sh --json "$ARGUMENTS"` 并带上计算出的编号和短名称：
      - 传递 `--number N+1` 和 `--short-name "your-short-name"` 以及功能描述
      - Bash 示例：`.specify/scripts/bash/create-new-feature.sh --json "$ARGUMENTS" --json --number 5 --short-name "user-auth" "Add user authentication"`