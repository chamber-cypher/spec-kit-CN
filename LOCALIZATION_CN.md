# Specify CLI 中文化指南

## 项目概述

本项目是 GitHub Spec Kit (specify-cli) 的中文化版本 Fork。目标是将命令行界面和用户提示文本从英文翻译为中文，以便中文用户更好地使用该工具。

## 实施方案

本项目采用 **方案 3A：国际化框架（i18n）+ Fork**

### 方案概述

不直接硬编码中文，而是通过国际化框架实现多语言支持，这样可以：
- ✅ **易于维护**：上游更新时不会产生大量翻译冲突
- ✅ **可切换语言**：通过环境变量在中英文间切换
- ✅ **易于扩展**：可以轻松添加更多语言
- ✅ **可贡献上游**：可以将国际化框架贡献回原项目

### 实施步骤

1. **Fork 仓库**
   - 已从 `github/spec-kit` 创建 fork
   - Fork 地址：`YOUR_USERNAME/spec-kit`（请替换为实际的 GitHub 用户名）

2. **添加国际化支持**
   - 创建翻译模块：`src/specify_cli/i18n.py`
   - 定义翻译字典（英文、中文等）
   - 提供翻译函数 `t(key)`

3. **重构源代码**
   - 修改 `src/specify_cli/__init__.py`
   - 将硬编码文本改为调用 `t()` 函数
   - 原代码：`"Project Setup"`
   - 改为：`t('project_setup')`

4. **安装使用**
   ```bash
   # 从您的 fork 安装
   uv tool install specify-cli --from git+https://github.com/YOUR_USERNAME/spec-kit.git
   
   # 或从本地开发版本安装
   cd /Users/perlied/Documents/smsbus/spec-kit-CN
   uv tool install specify-cli --from .
   
   # 使用中文版
   SPECIFY_LANG=zh_CN specify init my-project
   
# 或使用 CLI 别名（自动设置中文）
specify_cn init my-project

> `specify_cn` 会在启动 CLI 之前自动设置 `SPECIFY_LANG=zh_CN`，因此无需手动导出环境变量。

   # 使用英文版（默认）
   specify init my-project
   ```

### 架构设计

```
spec-kit-CN/
├── src/
│   └── specify_cli/
│       ├── __init__.py          # 主程序（调用 t() 函数）
│       └── i18n.py              # 国际化模块（包含所有翻译）
```

**翻译流程：**
```
用户执行命令 → 读取 SPECIFY_LANG 环境变量 → 加载对应语言字典 → 显示翻译文本
```

## 已完成的工作

### 1. 创建文档和规划
- ✅ 创建 `LOCALIZATION_CN.md` 中文化指南
- ✅ 确定使用 i18n 框架方案
- ✅ 规划翻译内容和实施步骤

### 2. 初步修改（如有）
已修改文件：`src/specify_cli/__init__.py`

#### 已翻译的部分：

1. **项目设置面板** (约第 949 行)
   - 已修改为中文（待重构为 i18n 方式）
   - "Specify Project Setup" → "Specify 项目设置"
   - "Project" → "项目"
   - "Working Path" → "工作路径"
   - "Target Path" → "目标路径"

**注意**：如果已经直接修改了源码，需要按照下面的"待完成工作"重构为 i18n 框架方式。

## 待完成的工作

### 阶段 1：创建 i18n 框架（优先级：高）

#### 1.1 创建翻译模块 `src/specify_cli/i18n.py`

需要实现以下功能：

```python
import os

# 完整的翻译字典
TRANSLATIONS = {
    'en': {
        # 项目设置
        'project_setup': 'Specify Project Setup',
        'project': 'Project',
        'working_path': 'Working Path',
        # ... 所有英文文本
    },
    'zh_CN': {
        # 项目设置
        'project_setup': 'Specify 项目设置',
        'project': '项目',
        'working_path': '工作路径',
        # ... 所有中文翻译
    }
}

# 翻译函数
def t(key: str) -> str:
    """获取翻译文本"""
    lang = os.getenv('SPECIFY_LANG', 'en')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
```

**完整的翻译键清单**见下方"翻译内容清单"。

#### 1.2 修改主程序使用 i18n

在 `src/specify_cli/__init__.py` 中：

1. **导入翻译函数**
   ```python
   from .i18n import t
   ```

2. **重构所有硬编码文本**
   - 将 `"Specify Project Setup"` 改为 `t('project_setup')`
   - 将 `"Project"` 改为 `t('project')`
   - 依此类推...

### 阶段 2：翻译内容清单

以下是需要添加到 `i18n.py` 翻译字典的所有键值对：

#### 2.1 选择提示文本 (约第 968-987 行)
```python
# i18n.py 中添加：
'choose_ai_assistant': {
    'en': 'Choose your AI assistant:',
    'zh_CN': '选择您的 AI 助手：'
},
'choose_script_type': {
    'en': 'Choose script type (or press Enter)',
    'zh_CN': '选择脚本类型（或按回车使用默认）'
}

# __init__.py 中修改为：
selected_ai = select_with_arrows(ai_choices, t('choose_ai_assistant'), "copilot")
selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, t('choose_script_type'), default_script)
```

#### 2.2 状态消息 (约第 1010-1022 行)
```python
# i18n.py 中添加：
'selected_ai': {
    'en': 'Selected AI assistant:',
    'zh_CN': '已选择 AI 助手:'
},
'selected_script': {
    'en': 'Selected script type:',
    'zh_CN': '已选择脚本类型:'
}

# __init__.py 中修改为：
console.print(f"[cyan]{t('selected_ai')}[/cyan] {selected_ai}")
console.print(f"[cyan]{t('selected_script')}[/cyan] {selected_script}")
```

#### 2.3 步骤跟踪器标题和步骤 (约第 1014-1034 行)
```python
# i18n.py 中添加：
'initialize_project': {
    'en': 'Initialize Specify Project',
    'zh_CN': '初始化 Specify 项目'
},
'check_tools': {
    'en': 'Check required tools',
    'zh_CN': '检查必需工具'
},
'select_ai': {
    'en': 'Select AI assistant',
    'zh_CN': '选择 AI 助手'
},
'select_script': {
    'en': 'Select script type',
    'zh_CN': '选择脚本类型'
},
'fetch_release': {
    'en': 'Fetch latest release',
    'zh_CN': '获取最新版本'
},
'download_template': {
    'en': 'Download template',
    'zh_CN': '下载模板'
},
'extract_template': {
    'en': 'Extract template',
    'zh_CN': '解压模板'
},
'archive_contents': {
    'en': 'Archive contents',
    'zh_CN': '归档内容'
},
'extraction_summary': {
    'en': 'Extraction summary',
    'zh_CN': '解压摘要'
},
'ensure_executable': {
    'en': 'Ensure scripts executable',
    'zh_CN': '确保脚本可执行'
},
'cleanup': {
    'en': 'Cleanup',
    'zh_CN': '清理'
},
'init_git': {
    'en': 'Initialize git repository',
    'zh_CN': '初始化 git 仓库'
},
'finalize': {
    'en': 'Finalize',
    'zh_CN': '完成'
}

# __init__.py 中修改为：
tracker = StepTracker(t('initialize_project'))
tracker.add("precheck", t('check_tools'))
tracker.add("ai-select", t('select_ai'))
tracker.add("script-select", t('select_script'))
for key, trans_key in [
    ("fetch", "fetch_release"),
    ("download", "download_template"),
    ("extract", "extract_template"),
    ("zip-list", "archive_contents"),
    ("extracted-summary", "extraction_summary"),
    ("chmod", "ensure_executable"),
    ("cleanup", "cleanup"),
    ("git", "init_git"),
    ("final", "finalize")
]:
    tracker.add(key, t(trans_key))
```

#### 2.4 步骤完成状态消息 (约第 1018-1067 行)
```python
# i18n.py 中添加：
'status_ok': {
    'en': 'ok',
    'zh_CN': '完成'
},
'status_existing_repo': {
    'en': 'existing repo detected',
    'zh_CN': '检测到现有仓库'
},
'status_initialized': {
    'en': 'initialized',
    'zh_CN': '已初始化'
},
'status_init_failed': {
    'en': 'init failed',
    'zh_CN': '初始化失败'
},
'status_git_unavailable': {
    'en': 'git not available',
    'zh_CN': 'git 不可用'
},
'status_no_git_flag': {
    'en': '--no-git flag',
    'zh_CN': '--no-git 标志'
},
'status_project_ready': {
    'en': 'project ready',
    'zh_CN': '项目就绪'
}

# __init__.py 中修改为：
tracker.complete("precheck", t('status_ok'))
tracker.complete("git", t('status_existing_repo'))
tracker.complete("git", t('status_initialized'))
tracker.error("git", t('status_init_failed'))
tracker.skip("git", t('status_git_unavailable'))
tracker.skip("git", t('status_no_git_flag'))
tracker.complete("final", t('status_project_ready'))
```

#### 2.5 成功消息和错误面板 (约第 1085-1105 行)
```python
# i18n.py 中添加：
'project_ready_msg': {
    'en': 'Project ready.',
    'zh_CN': '项目就绪。'
},
'git_init_failed_title': {
    'en': 'Git Initialization Failed',
    'zh_CN': 'Git 初始化失败'
},
'git_init_skipped': {
    'en': 'Git repository initialization skipped:',
    'zh_CN': 'Git 仓库初始化已跳过:'
},
'git_manual_init': {
    'en': 'You can manually initialize git later with:',
    'zh_CN': '您可以稍后手动初始化 git:'
}

# __init__.py 中修改为：
console.print(f"\n[bold green]{t('project_ready_msg')}[/bold green]")

git_error_panel = Panel(
    f"{t('git_init_skipped')}\n[dim]{git_error_message}[/dim]\n\n"
    f"{t('git_manual_init')} [cyan]git init[/cyan]",
    title=f"[red]{t('git_init_failed_title')}[/red]",
    border_style="red",
    padding=(1, 2)
)
```

#### 2.6 安全提示面板 (约第 1106-1118 行)
```python
# i18n.py 中添加：
'agent_folder_security': {
    'en': 'Agent Folder Security',
    'zh_CN': '代理文件夹安全'
},
'security_notice_msg': {
    'en': 'Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\nConsider adding {folder} (or parts of it) to .gitignore to prevent accidental credential leakage.',
    'zh_CN': '某些 AI 助手可能会在项目的代理文件夹中存储凭据、身份验证令牌或其他敏感信息。\n建议将 {folder}（或其部分内容）添加到 .gitignore 以防止意外泄露凭据。'
}

# __init__.py 中修改为：
security_notice = Panel(
    t('security_notice_msg').format(
        folder=f"[cyan]{agent_folder}[/cyan]"
    ),
    title=f"[yellow]{t('agent_folder_security')}[/yellow]",
    border_style="yellow",
    padding=(1, 2)
)
```

#### 2.7 后续步骤面板 (约第 1120-1148 行)
```python
# i18n.py 中添加：
'next_steps': {
    'en': 'Next Steps',
    'zh_CN': '后续步骤'
},
'go_to_project': {
    'en': 'Go to the project folder:',
    'zh_CN': '进入项目文件夹:'
},
'already_in_directory': {
    'en': "You're already in the project directory!",
    'zh_CN': '您已经在项目目录中！'
},
'set_codex_home': {
    'en': 'Set CODEX_HOME environment variable before running Codex:',
    'zh_CN': '在运行 Codex 前设置 CODEX_HOME 环境变量:'
},
'start_using_commands': {
    'en': 'Start using slash commands with your AI agent:',
    'zh_CN': '开始使用 AI 助手的斜杠命令:'
},
'cmd_constitution': {
    'en': 'Establish project principles',
    'zh_CN': '建立项目原则'
},
'cmd_specify': {
    'en': 'Create baseline specification',
    'zh_CN': '创建基准规范'
},
'cmd_plan': {
    'en': 'Create implementation plan',
    'zh_CN': '创建实施计划'
},
'cmd_tasks': {
    'en': 'Generate actionable tasks',
    'zh_CN': '生成可执行任务'
},
'cmd_implement': {
    'en': 'Execute implementation',
    'zh_CN': '执行实施'
}

# __init__.py 中修改为：
if not here:
    steps_lines.append(f"1. {t('go_to_project')} [cyan]cd {project_name}[/cyan]")
else:
    steps_lines.append(f"1. {t('already_in_directory')}")

if selected_ai == "codex":
    steps_lines.append(f"{step_num}. {t('set_codex_home')} [cyan]{cmd}[/cyan]")

steps_lines.append(f"{step_num}. {t('start_using_commands')}")
steps_lines.append(f"   2.1 [cyan]/speckit.constitution[/] - {t('cmd_constitution')}")
steps_lines.append(f"   2.2 [cyan]/speckit.specify[/] - {t('cmd_specify')}")
steps_lines.append(f"   2.3 [cyan]/speckit.plan[/] - {t('cmd_plan')}")
steps_lines.append(f"   2.4 [cyan]/speckit.tasks[/] - {t('cmd_tasks')}")
steps_lines.append(f"   2.5 [cyan]/speckit.implement[/] - {t('cmd_implement')}")

steps_panel = Panel("\n".join(steps_lines), title=t('next_steps'), border_style="cyan", padding=(1,2))
```

#### 2.8 增强命令面板 (约第 1150-1160 行)
```python
# i18n.py 中添加：
'enhancement_commands': {
    'en': 'Enhancement Commands',
    'zh_CN': '增强命令'
},
'optional_commands_desc': {
    'en': 'Optional commands that you can use for your specs (improve quality & confidence)',
    'zh_CN': '可用于规范的可选命令（提高质量和可信度）'
},
'optional': {
    'en': 'optional',
    'zh_CN': '可选'
},
'cmd_clarify_desc': {
    'en': 'Ask structured questions to de-risk ambiguous areas before planning (run before /speckit.plan if used)',
    'zh_CN': '在规划前询问结构化问题以降低模糊区域的风险（如使用，请在 /speckit.plan 之前运行）'
},
'cmd_analyze_desc': {
    'en': 'Cross-artifact consistency & alignment report (after /speckit.tasks, before /speckit.implement)',
    'zh_CN': '跨工件一致性和对齐报告（在 /speckit.tasks 之后、/speckit.implement 之前）'
},
'cmd_checklist_desc': {
    'en': 'Generate quality checklists to validate requirements completeness, clarity, and consistency (after /speckit.plan)',
    'zh_CN': '生成质量检查清单以验证需求的完整性、清晰度和一致性（在 /speckit.plan 之后）'
}

# __init__.py 中修改为：
enhancement_lines = [
    f"{t('optional_commands_desc')}",
    "",
    f"○ [cyan]/speckit.clarify[/] [bright_black]({t('optional')})[/bright_black] - {t('cmd_clarify_desc')}",
    f"○ [cyan]/speckit.analyze[/] [bright_black]({t('optional')})[/bright_black] - {t('cmd_analyze_desc')}",
    f"○ [cyan]/speckit.checklist[/] [bright_black]({t('optional')})[/bright_black] - {t('cmd_checklist_desc')}"
]
enhancements_panel = Panel("\n".join(enhancement_lines), title=t('enhancement_commands'), border_style="cyan", padding=(1,2))
```

#### 2.9 check 命令翻译 (约第 1162-1199 行)
```python
# i18n.py 中添加：
'check_tools_docstring': {
    'en': 'Check that all required tools are installed.',
    'zh_CN': '检查是否安装了所有必需的工具。'
},
'checking_tools': {
    'en': 'Checking for installed tools...',
    'zh_CN': '正在检查已安装的工具...'
},
'check_available_tools': {
    'en': 'Check Available Tools',
    'zh_CN': '检查可用工具'
},
'git_version_control': {
    'en': 'Git version control',
    'zh_CN': 'Git 版本控制'
},
'ide_based_no_cli': {
    'en': 'IDE-based, no CLI check',
    'zh_CN': '基于 IDE，无需 CLI 检查'
},
'cli_ready': {
    'en': 'Specify CLI is ready to use!',
    'zh_CN': 'Specify CLI 已就绪！'
},
'tip_install_git': {
    'en': 'Tip: Install git for repository management',
    'zh_CN': '提示: 安装 git 以进行仓库管理'
},
'tip_install_assistant': {
    'en': 'Tip: Install an AI assistant for the best experience',
    'zh_CN': '提示: 安装 AI 助手以获得最佳体验'
}

# __init__.py 中修改为：
@app.command()
def check():
    """使用 t('check_tools_docstring') 在代码中动态获取"""
    show_banner()
    console.print(f"[bold]{t('checking_tools')}[/bold]\n")
    
    tracker = StepTracker(t('check_available_tools'))
    tracker.add("git", t('git_version_control'))
    # ...
    tracker.skip(agent_key, t('ide_based_no_cli'))
    # ...
    
    console.print(f"\n[bold green]{t('cli_ready')}[/bold green]")
    
    if not git_ok:
        console.print(f"[dim]{t('tip_install_git')}[/dim]")
    
    if not any(agent_results.values()):
        console.print(f"[dim]{t('tip_install_assistant')}[/dim]")
```

### 阶段 3：其他需要翻译的内容

#### 3.1 错误消息和警告

需要搜索 `__init__.py` 文件中所有的错误消息、警告和提示，例如：
- `console.print("[red]Error:[/red] ...")`
- `Panel(..., title="[red]...[/red]")`
- `raise typer.Exit(1)` 之前的消息
- 所有 `console.print("[yellow]...")` 警告消息

#### 3.2 命令帮助文本和文档字符串

所有 Typer 命令的帮助文本：
```python
@app.command()
def init(...):
    """Initialize a new Specify project."""  # 需要翻译
    
@app.command()
def check():
    """Check that all required tools are installed."""  # 需要翻译
```

**注意**：Typer 的文档字符串可能需要特殊处理，或者保持英文（因为命令本身是英文）。

#### 3.3 Banner 和品牌信息

查找 `show_banner()` 函数，确认是否需要翻译 banner 中的文本（通常品牌名称保持原样）。

### 阶段 4：创建完整的翻译文件模板

基于以上所有翻译键，创建完整的 `i18n.py` 文件（约 100+ 个翻译项）。

详见文档末尾的"完整 i18n.py 模板"。

## 翻译原则

1. **保持格式标记**：所有 Rich 库的格式标记（如 `[cyan]`、`[bold]` 等）必须保持不变
2. **保持命令和路径**：所有命令名称（如 `/speckit.constitution`）、文件路径保持英文
3. **保持技术术语**：如 "git"、"repository"（可译为"仓库"）、"CLI" 等
4. **简洁明了**：中文翻译应简洁、符合中文表达习惯
5. **一致性**：相同的英文术语在整个项目中应使用相同的中文翻译

## 测试步骤

完成翻译后，需要进行以下测试：

1. **安装测试**
```bash
cd /Users/perlied/Documents/smsbus/spec-kit-CN
uv tool uninstall specify-cli
uv tool install specify-cli --from .
```

2. **功能测试**
```bash
# 创建测试目录
cd /tmp
mkdir test-specify-cn
cd test-specify-cn

# 运行初始化命令
specify init .

# 检查所有输出是否为中文
# 测试各个斜杠命令是否正常工作
```

3. **验证清单**
   - [ ] 所有面板标题都是中文
   - [ ] 步骤跟踪器的步骤名称都是中文
   - [ ] 状态消息（完成、跳过、错误）都是中文
   - [ ] 错误提示都是中文
   - [ ] 帮助文本都是中文
   - [ ] 命令描述都是中文
   - [ ] 后续步骤说明都是中文

## 发布流程

### 1. 创建分支
```bash
cd /Users/perlied/Documents/smsbus/spec-kit-CN
git checkout -b feat/chinese-localization
```

### 2. 提交更改
```bash
git add src/specify_cli/__init__.py LOCALIZATION_CN.md
git commit -m "feat: 添加中文本地化支持

- 翻译所有用户界面文本为中文
- 包括：项目设置、步骤跟踪、错误消息、帮助文本等
- 添加中文化文档说明
"
```

### 3. 推送到您的 Fork
```bash
# 替换 YOUR_USERNAME 为您的 GitHub 用户名
git push origin feat/chinese-localization
```

### 4. 合并到主分支（可选）
```bash
git checkout main
git merge feat/chinese-localization
git push origin main
```

### 5. 安装和使用

**方式一：从 GitHub 安装（推荐给其他用户）**
```bash
# 卸载旧版本
uv tool uninstall specify-cli

# 从您的 fork 主分支安装
uv tool install specify-cli --from git+https://github.com/YOUR_USERNAME/spec-kit.git

# 或从特定分支安装
uv tool install specify-cli --from git+https://github.com/YOUR_USERNAME/spec-kit.git@feat/chinese-localization
```

**方式二：从本地安装（用于开发测试）**
```bash
cd /Users/perlied/Documents/smsbus/spec-kit-CN
uv tool uninstall specify-cli
uv tool install specify-cli --from .
```

### 6. 更新 README
在您的 fork 的 README.md 中添加中文使用说明：

```markdown
# Spec Kit - 中文版

这是 GitHub Spec Kit 的中文化版本。

## 安装

```bash
uv tool install specify-cli --from git+https://github.com/YOUR_USERNAME/spec-kit.git
```

## 使用

所有命令和提示都已翻译为中文：

```bash
# 初始化项目
specify init my-project

# 查看帮助
specify --help
```

## 与上游同步

本项目定期从 [github/spec-kit](https://github.com/github/spec-kit) 同步更新。

## 贡献

欢迎提交问题和改进建议！
```

## 后续维护

### 同步上游更新

定期从原始仓库同步更新：

```bash
cd /Users/perlied/Documents/smsbus/spec-kit-CN

# 添加上游仓库（首次执行）
git remote add upstream https://github.com/github/spec-kit.git

# 获取上游更新
git fetch upstream

# 查看上游变更
git log upstream/main --oneline

# 合并上游更新到您的主分支
git checkout main
git merge upstream/main

# 解决冲突（如果有）
# 主要关注 src/specify_cli/__init__.py 文件
# 保留中文翻译，同时合并新功能

# 推送更新
git push origin main
```

### 维护清单

- [ ] 每月检查上游更新
- [ ] 测试新功能是否正常工作
- [ ] 更新中文翻译以匹配新功能
- [ ] 更新 LOCALIZATION_CN.md 文档
- [ ] 通知用户重新安装以获取更新

### 未来增强

考虑的改进方向：

1. **添加语言切换功能**
   - 通过环境变量或配置文件选择语言
   - `SPECIFY_LANG=zh_CN specify init`

2. **国际化 (i18n) 框架**
   - 使用 gettext 或类似工具
   - 支持多语言切换

3. **贡献回上游**
   - 将国际化框架贡献给原项目
   - 让更多语言的用户受益

## 更好的实施方案：国际化框架

### 问题：硬编码中文的弊端

当前方案（直接修改源码为中文）存在的问题：
- ❌ **维护困难**：每次上游更新都需要重新翻译
- ❌ **无法切换语言**：用户无法在中英文之间切换
- ❌ **难以贡献**：无法合并回上游项目
- ❌ **容易冲突**：合并上游更新时会产生大量冲突

### 推荐方案：使用国际化框架

#### 方案 3A：使用字典映射 + 环境变量（推荐）

这是最简单且易于维护的方案：

**实现步骤：**

1. **创建翻译文件** `src/specify_cli/i18n.py`
```python
import os

# 翻译字典
TRANSLATIONS = {
    'en': {
        'project_setup': 'Specify Project Setup',
        'project': 'Project',
        'working_path': 'Working Path',
        'target_path': 'Target Path',
        'selected_ai': 'Selected AI assistant:',
        'selected_script': 'Selected script type:',
        'initialize_project': 'Initialize Specify Project',
        'check_tools': 'Check required tools',
        'select_ai': 'Select AI assistant',
        'select_script': 'Select script type',
        'fetch_release': 'Fetch latest release',
        'download_template': 'Download template',
        'extract_template': 'Extract template',
        'archive_contents': 'Archive contents',
        'extraction_summary': 'Extraction summary',
        'ensure_executable': 'Ensure scripts executable',
        'cleanup': 'Cleanup',
        'init_git': 'Initialize git repository',
        'finalize': 'Finalize',
        'project_ready': 'Project ready.',
        'next_steps': 'Next Steps',
        'enhancement_commands': 'Enhancement Commands',
        # ... 更多翻译
    },
    'zh_CN': {
        'project_setup': 'Specify 项目设置',
        'project': '项目',
        'working_path': '工作路径',
        'target_path': '目标路径',
        'selected_ai': '已选择 AI 助手:',
        'selected_script': '已选择脚本类型:',
        'initialize_project': '初始化 Specify 项目',
        'check_tools': '检查必需工具',
        'select_ai': '选择 AI 助手',
        'select_script': '选择脚本类型',
        'fetch_release': '获取最新版本',
        'download_template': '下载模板',
        'extract_template': '解压模板',
        'archive_contents': '归档内容',
        'extraction_summary': '解压摘要',
        'ensure_executable': '确保脚本可执行',
        'cleanup': '清理',
        'init_git': '初始化 git 仓库',
        'finalize': '完成',
        'project_ready': '项目就绪。',
        'next_steps': '后续步骤',
        'enhancement_commands': '增强命令',
        # ... 更多翻译
    }
}

# 获取当前语言
def get_language():
    """从环境变量获取语言设置，默认为英文"""
    return os.getenv('SPECIFY_LANG', 'en')

# 翻译函数
def t(key: str) -> str:
    """获取翻译文本"""
    lang = get_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

# 或者使用类
class I18n:
    def __init__(self):
        self.lang = get_language()
    
    def t(self, key: str) -> str:
        return TRANSLATIONS.get(self.lang, TRANSLATIONS['en']).get(key, key)
    
    def __call__(self, key: str) -> str:
        return self.t(key)

# 创建全局实例
i18n = I18n()
```

2. **修改 `__init__.py` 使用翻译函数**
```python
from .i18n import t  # 或 from .i18n import i18n

# 原来的代码
setup_lines = [
    "[cyan]Specify Project Setup[/cyan]",
    ...
]

# 改为
setup_lines = [
    f"[cyan]{t('project_setup')}[/cyan]",
    ...
]

# 或使用 i18n 实例
setup_lines = [
    f"[cyan]{i18n('project_setup')}[/cyan]",
    ...
]
```

3. **使用方式**
```bash
# 英文版（默认）
specify init my-project

# 中文版
SPECIFY_LANG=zh_CN specify init my-project

# 或设置永久环境变量
export SPECIFY_LANG=zh_CN
specify init my-project
```

**优点：**
- ✅ **易于维护**：翻译集中管理，一目了然
- ✅ **可切换语言**：通过环境变量轻松切换
- ✅ **易于同步**：上游更新只需修改 `__init__.py` 的调用，不影响翻译
- ✅ **易于扩展**：可以轻松添加更多语言
- ✅ **代码侵入小**：只需导入翻译函数并包装字符串

#### 方案 3B：使用 gettext（标准但复杂）

这是 Python 标准的国际化方案：

```python
import gettext
import os

# 设置翻译
locale_dir = os.path.join(os.path.dirname(__file__), 'locales')
lang = os.getenv('SPECIFY_LANG', 'en')

try:
    translation = gettext.translation('specify', locale_dir, languages=[lang])
    _ = translation.gettext
except FileNotFoundError:
    _ = lambda s: s  # 回退到原文

# 使用
setup_lines = [
    f"[cyan]{_('Specify Project Setup')}[/cyan]",
    ...
]
```

需要创建 `.po` 和 `.mo` 文件，配置更复杂。

#### 方案 3C：使用 Babel（专业方案）

适合大型项目，提供完整的国际化工具链。

### 推荐实施步骤

**第一阶段：最小化改动（现在可以做）**
1. 创建 `src/specify_cli/i18n.py` 翻译字典
2. 修改 `__init__.py` 中的关键用户界面文本使用 `t()` 函数
3. 测试中英文切换
4. 提交到您的 fork

**第二阶段：完善（后续迭代）**
1. 补充所有缺失的翻译项
2. 添加自动检测系统语言
3. 添加配置文件支持（除了环境变量）
4. 考虑贡献回上游

**第三阶段：贡献上游（最终目标）**
1. 完善国际化框架
2. 编写文档和测试
3. 提交 PR 到 `github/spec-kit`
4. 帮助更多语言的用户

### 代码重构示例

**原代码（硬编码）：**
```python
console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
tracker = StepTracker("Initialize Specify Project")
```

**重构后（使用 i18n）：**
```python
from .i18n import t

console.print(f"[cyan]{t('selected_ai')}[/cyan] {selected_ai}")
tracker = StepTracker(t('initialize_project'))
```

### 合并上游更新时

**使用硬编码（当前方案）：**
```bash
# 上游更新了这行
- console.print("New feature added")
# 您的版本是
- console.print("添加了新功能")
# 冲突！需要手动解决并重新翻译
```

**使用 i18n 框架：**
```bash
# 上游更新了这行
- console.print("New feature added")
# 您的版本是
- console.print(t('new_feature_added'))
# 可能不冲突，即使冲突也容易解决
# 只需在 i18n.py 中添加翻译即可
```

### 迁移策略

可以逐步迁移，不需要一次性改完：

```python
# 混合使用：已翻译的用 t()，未翻译的保持原样
console.print(f"[cyan]{t('project_setup')}[/cyan]")  # 已迁移
console.print("Some less important message")  # 暂未迁移
```

## 常见问题

### Q: 如何更新到最新版本？
```bash
uv tool uninstall specify-cli
uv tool install specify-cli --from git+https://github.com/YOUR_USERNAME/spec-kit.git
```

### Q: 如何在中英文版本间切换？
```bash
# 安装中文版
uv tool install specify-cli --from git+https://github.com/YOUR_USERNAME/spec-kit.git

# 切换回英文原版
uv tool uninstall specify-cli
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

### Q: 如何参与翻译改进？
1. Fork 本项目
2. 修改翻译
3. 提交 Pull Request
4. 或直接提 Issue 提出改进建议

### Q: 发现翻译错误怎么办？
请在 GitHub Issues 中报告，包括：
- 错误的翻译内容
- 出现位置（命令/场景）
- 建议的正确翻译

## 相关资源

- 原始仓库: https://github.com/github/spec-kit
- Fork 仓库: https://github.com/YOUR_USERNAME/spec-kit（请替换为实际地址）
- 本地路径: `/Users/perlied/Documents/smsbus/spec-kit-CN`
- Rich 库文档: https://rich.readthedocs.io/
- Typer 文档: https://typer.tiangolo.com/
- uv 工具文档: https://github.com/astral-sh/uv

## 快速命令参考

```bash
# 开发工作流
cd /Users/perlied/Documents/smsbus/spec-kit-CN
git status                          # 查看修改
git diff src/specify_cli/__init__.py # 查看具体改动
git add -A                          # 暂存所有修改
git commit -m "翻译更新"             # 提交
git push origin main                # 推送

# 测试工作流
uv tool uninstall specify-cli       # 卸载旧版
uv tool install specify-cli --from . # 从本地安装
cd /tmp && mkdir test-cn && cd test-cn # 创建测试目录
specify init .                      # 测试初始化
specify check                       # 测试检查命令

# 同步上游
git fetch upstream                  # 获取上游更新
git merge upstream/main             # 合并更新
```

---

**项目信息**
- **最后更新**: 2025年11月13日
- **维护者**: perlied
- **状态**: 进行中
- **完成度**: ~5% （已完成项目设置面板翻译）
- **下一步**: 继续翻译步骤跟踪器和状态消息

**联系方式**
- 如有问题或建议，请在 GitHub Issues 中提出
