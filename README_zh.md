<p align="center">
  <img src="https://img.shields.io/badge/版本-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/许可证-MIT-orange.svg" alt="许可证">
  <img src="https://img.shields.io/badge/零依赖-✓-brightgreen.svg" alt="零依赖">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_zh.md">简体中文</a> | 
  <a href="README_zh-tw.md">繁體中文</a>
</p>

<h1 align="center">🚀 CommitPilot</h1>

<p align="center">
  <strong>智能Git提交助手CLI</strong><br>
  <em>智能提交信息生成 • 零依赖 • 多语言支持</em>
</p>

---

## 🎉 项目介绍

**CommitPilot** 是一款轻量级、智能的Git提交助手，帮助开发者编写更好的提交信息。它会分析您的暂存更改，自动生成符合规范的、有意义的提交信息。

### 为什么选择CommitPilot？

- 🤖 **智能分析** - 智能检测提交类型、范围和主题
- 📝 **多种风格** - 支持Conventional Commits、Angular、GitMoji格式
- 🌍 **多语言** - 界面支持中英日韩西等多国语言
- ⚡ **零依赖** - 轻量级核心，无外部依赖
- 🔧 **Git钩子集成** - 通过prepare-commit-msg钩子自动生成信息

### 灵感来源

编写好的提交信息对项目可维护性至关重要，但往往枯燥且不一致。CommitPilot旨在解决这一痛点，通过自动化流程保持高质量、标准化的输出。

---

## ✨ 核心特性

### 🔍 智能变更分析
- **自动类型检测** - 检测 `feat`、`fix`、`docs`、`refactor` 等
- **范围检测** - 识别受影响的模块（api、ui、core等）
- **破坏性变更检测** - 警告潜在的破坏性更改

### 📝 多种提交风格
| 风格 | 示例 |
|------|------|
| Conventional | `feat(api): 添加用户认证功能` |
| Angular | `feat(api): 添加用户认证功能` |
| GitMoji | `✨ (api) 添加用户认证功能` |

### 🌍 国际化支持
- 🇺🇸 English
- 🇨🇳 简体中文
- 🇹🇼 繁體中文
- 🇯🇵 日本語
- 🇰🇷 한국어
- 🇪🇸 Español

### 📊 提交统计
- 追踪提交频率
- 分析提交类型分布
- 查看贡献者统计

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Git

### 安装方式

```bash
# 从PyPI安装
pip install commitpilot

# 或从源码安装
git clone https://github.com/gitstq/CommitPilot.git
cd CommitPilot
pip install -e .
```

### 基本用法

```bash
# 暂存您的更改
git add .

# 生成提交信息
commitpilot generate

# 一步完成生成和提交
commitpilot commit

# 使用GitMoji风格
commitpilot generate --style gitmoji

# 分析当前更改
commitpilot analyze

# 查看提交统计
commitpilot stats --days 30
```

---

## 📖 详细使用指南

### 生成命令

```bash
# 基本生成
commitpilot generate

# 指定风格
commitpilot generate --style conventional  # 默认
commitpilot generate --style angular
commitpilot generate --style gitmoji

# 覆盖检测到的类型
commitpilot generate --type feat

# 设置自定义范围
commitpilot generate --scope api

# 自定义主题
commitpilot generate --subject "添加新功能"

# 显示备选方案
commitpilot generate --alternatives

# JSON输出（用于脚本）
commitpilot generate --json
```

### 提交命令

```bash
# 生成并提交
commitpilot commit

# 提交前编辑信息
commitpilot commit --edit

# 预览模式（不实际提交）
commitpilot commit --dry-run
```

### 分析命令

```bash
# 分析暂存更改
commitpilot analyze

# JSON输出
commitpilot analyze --json
```

### 统计命令

```bash
# 最近30天（默认）
commitpilot stats

# 自定义周期
commitpilot stats --days 7
commitpilot stats --days 90
```

### Git钩子集成

```bash
# 安装prepare-commit-msg钩子
commitpilot hook install

# 卸载钩子
commitpilot hook uninstall
```

安装钩子后，每次运行 `git commit` 时，CommitPilot会自动为您生成提交信息！

### 语言支持

```bash
# 使用中文界面
commitpilot -l zh generate

# 使用日文界面
commitpilot -l ja generate
```

---

## 💡 设计思路

### 为什么零依赖？

CommitPilot设计为轻量级且可靠。通过避免外部依赖：
- ⚡ 更快的安装速度
- 🔒 无供应链风险
- 🎯 可预测的行为
- 📦 更小的占用空间

### 架构设计

```
commitpilot/
├── core.py          # 核心分析和生成逻辑
├── cli.py           # 命令行界面
├── i18n.py          # 国际化支持
└── templates/       # 提交风格模板
```

### 后续规划

- [ ] AI驱动的信息生成（OpenAI/Anthropic集成）
- [ ] 自定义提交模板
- [ ] 团队共享配置
- [ ] 提交信息校验
- [ ] 与主流IDE集成

---

## 📦 构建与部署

### 从源码构建

```bash
# 安装构建工具
pip install build

# 构建包
python -m build

# 输出在 dist/ 目录
```

### 运行测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 带覆盖率运行
pytest tests/ --cov=commitpilot
```

---

## 🤝 贡献指南

欢迎贡献！以下是开始方式：

1. **Fork** 本仓库
2. **创建** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 更改 (`commitpilot commit`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **提交** Pull Request

### 提交规范

本项目使用Conventional Commits规范。CommitPilot会帮助您遵循这一规范！

---

## 📄 开源协议

本项目采用MIT协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  由 <a href="https://github.com/gitstq">gitstq</a> 用 ❤️ 制作
</p>

<p align="center">
  <strong>⭐ 如果这个项目对您有帮助，请给个星标支持！⭐</strong>
</p>
