<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/zero%20dependencies-✓-brightgreen.svg" alt="Zero Dependencies">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_zh.md">简体中文</a> | 
  <a href="README_zh-tw.md">繁體中文</a>
</p>

<h1 align="center">🚀 CommitPilot</h1>

<p align="center">
  <strong>Intelligent Git Commit Assistant CLI</strong><br>
  <em>Smart Commit Message Generation • Zero Dependencies • Multi-Language Support</em>
</p>

---

## 🎉 Project Introduction

**CommitPilot** is a lightweight, intelligent Git commit assistant that helps developers write better commit messages. It analyzes your staged changes and generates meaningful, specification-compliant commit messages automatically.

### Why CommitPilot?

- 🤖 **AI-Powered Analysis** - Intelligently detects commit type, scope, and subject
- 📝 **Multiple Styles** - Supports Conventional Commits, Angular, and GitMoji formats
- 🌍 **Multi-Language** - UI supports English, Chinese, Japanese, Korean, Spanish
- ⚡ **Zero Dependencies** - Lightweight core with no external dependencies
- 🔧 **Git Hook Integration** - Auto-generate messages with prepare-commit-msg hook

### Inspiration

Writing good commit messages is crucial for project maintainability, but it's often tedious and inconsistent. CommitPilot was created to solve this pain point by automating the process while maintaining high-quality, standardized output.

---

## ✨ Core Features

### 🔍 Intelligent Change Analysis
- **Automatic Type Detection** - Detects `feat`, `fix`, `docs`, `refactor`, etc.
- **Scope Detection** - Identifies affected modules (api, ui, core, etc.)
- **Breaking Change Detection** - Warns about potential breaking changes

### 📝 Multiple Commit Styles
| Style | Example |
|-------|---------|
| Conventional | `feat(api): add user authentication` |
| Angular | `feat(api): add user authentication` |
| GitMoji | `✨ (api) add user authentication` |

### 🌍 Internationalization
- 🇺🇸 English
- 🇨🇳 简体中文
- 🇹🇼 繁體中文
- 🇯🇵 日本語
- 🇰🇷 한국어
- 🇪🇸 Español

### 📊 Commit Statistics
- Track commit frequency
- Analyze commit types distribution
- View contributor statistics

---

## 🚀 Quick Start

### Requirements
- Python 3.8+
- Git

### Installation

```bash
# Install from PyPI
pip install commitpilot

# Or install from source
git clone https://github.com/gitstq/CommitPilot.git
cd CommitPilot
pip install -e .
```

### Basic Usage

```bash
# Stage your changes
git add .

# Generate a commit message
commitpilot generate

# Generate and commit in one step
commitpilot commit

# Use GitMoji style
commitpilot generate --style gitmoji

# Analyze current changes
commitpilot analyze

# View commit statistics
commitpilot stats --days 30
```

---

## 📖 Detailed Usage Guide

### Generate Command

```bash
# Basic generation
commitpilot generate

# Specify style
commitpilot generate --style conventional  # default
commitpilot generate --style angular
commitpilot generate --style gitmoji

# Override detected type
commitpilot generate --type feat

# Set custom scope
commitpilot generate --scope api

# Custom subject
commitpilot generate --subject "add new feature"

# Show alternatives
commitpilot generate --alternatives

# JSON output (for scripts)
commitpilot generate --json
```

### Commit Command

```bash
# Generate and commit
commitpilot commit

# Edit message before committing
commitpilot commit --edit

# Dry run (preview without committing)
commitpilot commit --dry-run
```

### Analyze Command

```bash
# Analyze staged changes
commitpilot analyze

# JSON output
commitpilot analyze --json
```

### Stats Command

```bash
# Last 30 days (default)
commitpilot stats

# Custom period
commitpilot stats --days 7
commitpilot stats --days 90
```

### Git Hook Integration

```bash
# Install prepare-commit-msg hook
commitpilot hook install

# Uninstall hook
commitpilot hook uninstall
```

After installing the hook, every time you run `git commit`, CommitPilot will automatically generate a commit message for you!

### Language Support

```bash
# Use Chinese interface
commitpilot -l zh generate

# Use Japanese interface
commitpilot -l ja generate
```

---

## 💡 Design Philosophy

### Why Zero Dependencies?

CommitPilot is designed to be lightweight and reliable. By avoiding external dependencies:
- ⚡ Faster installation
- 🔒 No supply chain risks
- 🎯 Predictable behavior
- 📦 Smaller footprint

### Architecture

```
commitpilot/
├── core.py          # Core analysis and generation logic
├── cli.py           # Command-line interface
├── i18n.py          # Internationalization
└── templates/       # Commit style templates
```

### Future Roadmap

- [ ] AI-powered message generation (OpenAI/Anthropic integration)
- [ ] Custom commit templates
- [ ] Team shared configurations
- [ ] Commit message linting
- [ ] Integration with popular IDEs

---

## 📦 Build & Deployment

### Build from Source

```bash
# Install build tools
pip install build

# Build package
python -m build

# Output in dist/
```

### Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=commitpilot
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`commitpilot commit`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Commit Convention

This project uses Conventional Commits. CommitPilot will help you follow this convention!

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>

<p align="center">
  <strong>⭐ If this project helps you, please give it a star! ⭐</strong>
</p>
