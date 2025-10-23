# 🔍 Git License Scanner

一個命令列工具，用於自動掃描和識別 Git 儲存庫中的軟體授權，並評估授權風險。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## ✨ 特色功能

- 🔍 **自動掃描**: 自動尋找 LICENSE、COPYING 等授權檔案
- 🎯 **智慧辨識**: 辨識 15+ 種常見開源授權（MIT、GPL、Apache 等）
- ⚠️ **風險評估**: 自動評估授權風險等級（低/中/高）
- 🎨 **美化輸出**: 彩色終端輸出，清晰易讀
- 📊 **JSON 報告**: 支援 JSON 格式輸出，方便整合 CI/CD
- 💯 **信心度評估**: 輸出辨識結果的信心度百分比

## 📦 安裝

### 從原始碼安裝
```bash
git clone https://github.com/yourusername/git-license-scanner.git
cd git-license-scanner
pip install -e .
```

### 依賴套件

- Python 3.10+
- click
- GitPython
- rich
- colorama
- PyYAML
- requests

## 🚀 使用方法

### 基本用法
```bash
# 掃描當前目錄
license-scan .

# 掃描指定目錄
license-scan /path/to/repository

# 詳細模式（顯示授權說明）
license-scan . -v

# 顯示檔案內容
license-scan . --show-content
```

### JSON 輸出
```bash
# 輸出 JSON 到終端機
license-scan . --output json

# 輸出 JSON 到檔案
license-scan . --output json --output-file report.json
```

### 範例輸出
```
🔍 Git License Scanner v0.5
━━━━━━━━━━━━━━━━━━━━━━━━━━━

正在掃描: .

✓ 找到 1 個授權檔案

📄 LICENSE
   路徑: ./LICENSE
   大小: 1070 bytes

╭──────────────┬─────────┬────────────┬──────────╮
│ 授權類型      │ 信心度   │ 風險等級   │ 相容性   │
├──────────────┼─────────┼────────────┼──────────┤
│ MIT License  │ 100.0%  │ 低 ✓       │ 優秀     │
╰──────────────┴─────────┴────────────┴──────────╯

📊 掃描摘要:
   總檔案數: 1
   已識別: 1
   高風險: 0
   中風險: 0
   低風險: 1

⚖️ 風險評估:
   ✓ 良好: 所有授權都是低風險

✅ 掃描完成！
```

## 📚 支援的授權類型

### 低風險（可供商用）
- MIT License
- Apache License 2.0
- BSD 2-Clause / 3-Clause
- ISC License

### 中風險（部分限制）
- LGPL 2.1 / 3.0
- Mozilla Public License 2.0

### 高風險（強制開源）
- GPL 2.0 / 3.0
- AGPL 3.0

## 🏗️ 專案結構
```
git-license-scanner/
├── license_scanner/        # 主要程式碼
│   ├── __init__.py
│   ├── cli.py              # CLI 介面
│   ├── scanner.py          # 掃描引擎
│   └── licenses_db.py      # 授權資料庫
├── tests/                  # 測試
├── examples/               # 範例專案
├── setup.py                # 安裝設定
├── requirements.txt        # 依賴清單
└── README.md               # 說明文件
```

## 🛠️ 開發

### 設定開發環境
```bash
# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 以開發模式安裝
pip install -e .
```

### 執行測試
```bash
# 測試基本掃描
python license_scanner/scanner.py

# 測試授權資料庫
python license_scanner/licenses_db.py

# 測試 CLI
python license_scanner/cli.py
```

## 📖 使用情境

### 情境 1：開發前檢查依賴授權
在專案開始前檢查所有依賴套件的授權，避免引入不相容的授權。

### 情境 2：CI/CD 整合
```bash
# 在 CI/CD 流水線中自動檢查
license-scan . --output json --output-file license-report.json

# 如果發現高風險授權，中止建置
if [ "$(jq '.summary.high_risk' license-report.json)" -gt 0 ]; then
    echo "發現高風險授權！"
    exit 1
fi
```

### 情境 3：定期合規稽核
定期掃描所有專案，產生授權合規報告。

## 🤝 貢獻

歡迎貢獻！請遵循以下步驟：

1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📝 授權

此專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案

## 👥 團隊成員

此專案為 IM3014 Linux 系統管理實務課程的期末專案。

- [成員 A] - 待分配
- [成員 B] - 待分配
- [成員 C] - 待分配

## 🙏 致謝

- 感謝 [SPDX](https://spdx.org/) 提供授權清單
- 使用 [Click](https://click.palletsprojects.com/) 框架建立 CLI
- 使用 [Rich](https://rich.readthedocs.io/) 美化終端輸出

## 📧 聯絡

專案連結: [https://github.com/yrzheng0419/git-license-scanner](https://github.com/yourusername/git-license-scanner)

---

⭐ 如果這個專案對你有幫助，請給我們一個星星！