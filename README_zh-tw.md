<p align="center">
  <img src="https://img.shields.io/badge/版本-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/授權條款-MIT-orange.svg" alt="授權條款">
  <img src="https://img.shields.io/badge/零依賴-✓-brightgreen.svg" alt="零依賴">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_zh.md">简体中文</a> | 
  <a href="README_zh-tw.md">繁體中文</a>
</p>

<h1 align="center">🚀 CommitPilot</h1>

<p align="center">
  <strong>智慧型Git提交助手CLI</strong><br>
  <em>智慧提交訊息生成 • 零依賴 • 多語言支援</em>
</p>

---

## 🎉 專案介紹

**CommitPilot** 是一款輕量級、智慧型的Git提交助手，幫助開發者撰寫更好的提交訊息。它會分析您的暫存變更，自動產生符合規範的、有意義的提交訊息。

### 為什麼選擇CommitPilot？

- 🤖 **智慧分析** - 智慧偵測提交類型、範圍和主題
- 📝 **多種風格** - 支援Conventional Commits、Angular、GitMoji格式
- 🌍 **多語言** - 介面支援中英日韓西等多國語言
- ⚡ **零依賴** - 輕量級核心，無外部依賴
- 🔧 **Git鉤子整合** - 透過prepare-commit-msg鉤子自動產生訊息

### 靈感來源

撰寫好的提交訊息對專案可維護性至關重要，但往往枯燥且不一致。CommitPilot旨在解決這一痛點，透過自動化流程保持高品質、標準化的輸出。

---

## ✨ 核心特性

### 🔍 智慧變更分析
- **自動類型偵測** - 偵測 `feat`、`fix`、`docs`、`refactor` 等
- **範圍偵測** - 識別受影響的模組（api、ui、core等）
- **破壞性變更偵測** - 警告潛在的破壞性變更

### 📝 多種提交風格
| 風格 | 範例 |
|------|------|
| Conventional | `feat(api): 新增使用者認證功能` |
| Angular | `feat(api): 新增使用者認證功能` |
| GitMoji | `✨ (api) 新增使用者認證功能` |

### 🌍 國際化支援
- 🇺🇸 English
- 🇨🇳 简体中文
- 🇹🇼 繁體中文
- 🇯🇵 日本語
- 🇰🇷 한국어
- 🇪🇸 Español

### 📊 提交統計
- 追蹤提交頻率
- 分析提交類型分佈
- 檢視貢獻者統計

---

## 🚀 快速開始

### 環境需求
- Python 3.8+
- Git

### 安裝方式

```bash
# 從PyPI安裝
pip install commitpilot

# 或從原始碼安裝
git clone https://github.com/gitstq/CommitPilot.git
cd CommitPilot
pip install -e .
```

### 基本用法

```bash
# 暫存您的變更
git add .

# 產生提交訊息
commitpilot generate

# 一步完成產生和提交
commitpilot commit

# 使用GitMoji風格
commitpilot generate --style gitmoji

# 分析目前變更
commitpilot analyze

# 檢視提交統計
commitpilot stats --days 30
```

---

## 📖 詳細使用指南

### 產生命令

```bash
# 基本產生
commitpilot generate

# 指定風格
commitpilot generate --style conventional  # 預設
commitpilot generate --style angular
commitpilot generate --style gitmoji

# 覆蓋偵測到的類型
commitpilot generate --type feat

# 設定自訂範圍
commitpilot generate --scope api

# 自訂主題
commitpilot generate --subject "新增新功能"

# 顯示備選方案
commitpilot generate --alternatives

# JSON輸出（用於腳本）
commitpilot generate --json
```

### 提交命令

```bash
# 產生並提交
commitpilot commit

# 提交前編輯訊息
commitpilot commit --edit

# 預覽模式（不實際提交）
commitpilot commit --dry-run
```

### 分析命令

```bash
# 分析暫存變更
commitpilot analyze

# JSON輸出
commitpilot analyze --json
```

### 統計命令

```bash
# 最近30天（預設）
commitpilot stats

# 自訂週期
commitpilot stats --days 7
commitpilot stats --days 90
```

### Git鉤子整合

```bash
# 安裝prepare-commit-msg鉤子
commitpilot hook install

# 解除安裝鉤子
commitpilot hook uninstall
```

安裝鉤子後，每次執行 `git commit` 時，CommitPilot會自動為您產生提交訊息！

### 語言支援

```bash
# 使用中文介面
commitpilot -l zh generate

# 使用日文介面
commitpilot -l ja generate
```

---

## 💡 設計思路

### 為什麼零依賴？

CommitPilot設計為輕量級且可靠。透過避免外部依賴：
- ⚡ 更快的安裝速度
- 🔒 無供應鏈風險
- 🎯 可預測的行為
- 📦 更小的佔用空間

### 架構設計

```
commitpilot/
├── core.py          # 核心分析和產生邏輯
├── cli.py           # 命令列介面
├── i18n.py          # 國際化支援
└── templates/       # 提交風格範本
```

### 後續規劃

- [ ] AI驅動的訊息產生（OpenAI/Anthropic整合）
- [ ] 自訂提交範本
- [ ] 團隊共享設定
- [ ] 提交訊息驗證
- [ ] 與主流IDE整合

---

## 📦 建置與部署

### 從原始碼建置

```bash
# 安裝建置工具
pip install build

# 建置套件
python -m build

# 輸出在 dist/ 目錄
```

### 執行測試

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest tests/ -v

# 帶覆蓋率執行
pytest tests/ --cov=commitpilot
```

---

## 🤝 貢獻指南

歡迎貢獻！以下是開始方式：

1. **Fork** 本儲存庫
2. **建立** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 變更 (`commitpilot commit`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **提交** Pull Request

### 提交規範

本專案使用Conventional Commits規範。CommitPilot會幫助您遵循這一規範！

---

## 📄 開源授權

本專案採用MIT授權條款開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  由 <a href="https://github.com/gitstq">gitstq</a> 用 ❤️ 製作
</p>

<p align="center">
  <strong>⭐ 如果這個專案對您有幫助，請給個星標支援！⭐</strong>
</p>
