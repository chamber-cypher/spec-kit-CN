# Spec Kit 中文版（spec-kit-CN）

本仓库是 [github/spec-kit](https://github.com/github/spec-kit) 的中文化 Fork，原先的英文的版本在vscode的copilot的初始页里显示不全。

## 🧬 Fork 来源与定位

| 项目 | 地址 | 说明 |
| --- | --- | --- |
| 上游（官方） | https://github.com/github/spec-kit | 原版 Spec Kit，专注于规范驱动开发流程 |
| 本仓库（Fork） | https://github.com/chamber-cypher/spec-kit-CN | 在上游基础上增加中文支持、i18n 框架与文档 |

保持与上游主分支同步是我们的长期工作：每次更新都会先合并 upstream 变更，再追加中文相关的功能或修复。

## ✨ 主要改动

1. **i18n 模块**：新增 `src/specify_cli/i18n.py`，集中管理翻译键值，所有 CLI 输出通过 `t()` 获取，支持 `SPECIFY_LANG=en|zh_CN` 切换。
2. **双入口命令**：
    - `specify`：保持上游英文体验；
    - `specify_cn`：在运行前自动设置 `SPECIFY_LANG=zh_CN`，即开即用中文界面。
3. **文档与指南**：`LOCALIZATION_CN.md` 记录中文化策略，本 README 重新介绍 Fork 背景、差异与使用方式。
4. **构建脚本同步**：`pyproject.toml` 增加中文入口脚本，`CHANGELOG.md` 遵循 Keep a Changelog 记录每次 i18n 相关发布。

## ⚙️ 安装方式

### 先决条件

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推荐）
- Git

### 从 GitHub Fork 安装

```bash
uv tool install specify-cli --from git+https://github.com/chamber-cypher/spec-kit-CN.git
```

### 从本地源码安装（开发调试）

```bash
cd /path/to/spec-kit-CN
uv tool install specify-cli --from .
```

升级或覆盖安装时可追加 `--force`。

## 🚀 使用说明

| 语言 | 命令 | 说明 |
| --- | --- | --- |
| 中文 | `specify_cn` | 自动切换 `SPECIFY_LANG=zh_CN`，输出与提示为中文 |
| 英文 | `specify` | 与上游一致，如需英文可保持默认或显式设置 `SPECIFY_LANG=en` |

常见示例：

```bash
# 初始化中文项目
specify_cn init my-project

# 在中文模式下查看帮助
specify_cn --help

# 强制使用中文但仍调用 specify 命令
SPECIFY_LANG=zh_CN specify check

# 恢复英文（默认）
specify init demo --ai copilot
```

> `specify_cn` 适合绝大多数中文场景；若想脚本化控制语言，可直接设置 `SPECIFY_LANG` 环境变量。

## 📦 目录速览

```
src/
├── specify_cli/            # 上游 CLI 主入口，字符串已接入 t()
│   ├── __init__.py
│   └── i18n.py             # 翻译字典、语言检测、t() Helper
├── specify_cli_cn/         # 中文入口模块（specify_cn 命令实际调用）
└── specify_cli_cn_entry.py # shim，兼容旧引用
```

其他重要文件：

- `LOCALIZATION_CN.md`：详细记录中文化方案与实施进度。
- `CHANGELOG.md`：每次版本变更（含 i18n 特性）都会记录。
- `templates/`：与上游保持一致的规范驱动开发模版。

## 🧪 开发与验证流程

1. **安装依赖**（如需隔离环境可使用 `uv venv`）：
    ```bash
    uv sync  # 或自行创建虚拟环境
    ```
2. **语法检查**：
    ```bash
    PYTHONPATH=src python -m compileall src/specify_cli src/specify_cli_cn
    ```
3. **本地回归**：
    ```bash
    uv tool uninstall specify-cli
    uv tool install specify-cli --from .
    specify_cn --help
    specify --help
    ```
4. **手动体验**（建议在临时目录）：
    ```bash
    mkdir -p /tmp/spec-kit-cn && cd /tmp/spec-kit-cn
    specify_cn init my-app
    specify_cn check
    ```

## 🔄 与上游同步

```bash
git remote add upstream https://github.com/github/spec-kit.git  # 首次执行
git fetch upstream
git checkout main
git merge upstream/main
# 解决冲突后，重新运行 uv install & specify_cn --help 确认中文依然生效
```

同步后请根据需要更新 `CHANGELOG.md` 与 `LOCALIZATION_CN.md`，确保 Fork 的改动透明可追踪。

## 🤝 贡献指南

- **翻译补全**：若发现 CLI 输出仍为英文，可在 `i18n.py` 中补充键值，并于 `__init__.py` 引用 `t()`。
- **文档改进**：补充中文教程、FAQ 或命令示例，欢迎直接更新 README 与 docs。
- **Issue/PR**：提交前请附上 `SPECIFY_LANG` 设置及复现步骤，方便定位问题。

## 📄 许可证 & 致谢

- 许可证：沿用上游的 [MIT License](./LICENSE)。
- 特别感谢 GitHub Spec Kit 团队以及所有提供中文化反馈的贡献者。

---

如需深入了解国际化方案或贡献流程，请参阅 [`LOCALIZATION_CN.md`](./LOCALIZATION_CN.md)。祝使用愉快！

