# Git License Scanner 使用指南

## 快速開始

### 安裝
```bash
pip install -e .
```

### 基本使用
```bash
license-scan .
```

## 命令列選項

### --output, -o
指定輸出格式：`text` 或 `json`
```bash
license-scan . --output json
```

### --output-file
將輸出儲存到檔案
```bash
license-scan . --output json --output-file report.json
```

### --verbose, -v
顯示詳細資訊
```bash
license-scan . -v
```

### --show-content
顯示授權檔案內容
```bash
license-scan . --show-content
```

## 常見問題

### Q: 為什麼無法識別授權？
A: 可能的原因：
- LICENSE 檔案內容不完整
- 使用了不常見的授權類型
- 授權文字被修改過

### Q: 信心度是什麼意思？
A: 信心度表示識別結果的可靠程度：
- 90-100%：非常確定
- 70-90%：可能正確
- 50-70%：不太確定
- <50%：建議手動確認

### Q: 如何在 CI/CD 中使用？
A: 範例：
```bash
license-scan . --output json --output-file report.json
if [ "$(jq '.summary.high_risk' report.json)" -gt 0 ]; then
    exit 1
fi
```

## 授權風險等級說明

### 低風險 🟢
適合商業使用，無需開源

### 中風險 🟡
部分情況需要開源，請仔細閱讀授權條款

### 高風險 🔴
強制開源，不適合閉源商業產品
```

儲存後離開。

---

## 📚 階段 4 總結

恭喜你完成最後階段！你的專案現在：

✅ **功能完整**
- 文字輸出（彩色、表格）
- JSON 輸出（方便程式化使用）
- 信心度警告
- 風險評估

✅ **可安裝使用**
- setup.py 設定完成
- 可以用 `pip install` 安裝
- 全域命令 `license-scan` 可用

✅ **文件完善**
- 專業的 README.md
- 使用者指南
- 程式碼註解清楚

✅ **展示就緒**
- demo.sh 展示腳本
- 多個測試範例
- JSON 報告輸出

---

## 🗂️ 最終專案結構
```
git-license-scanner/
├── LICENSE                         ← MIT 授權
├── README.md                       ← 專業版說明文件 ★
├── setup.py                        ← 安裝設定 ★
├── requirements.txt
├── .gitignore                      ← Git 忽略檔案 ★
├── demo.sh                         ← 展示腳本 ★
├── report.json                     ← 測試生成的報告
├── venv/
├── license_scanner/
│   ├── __init__.py                 ← 套件初始化 ★
│   ├── cli_v5.py                   ← 最終版 CLI ★
│   ├── scanner.py
│   └── licenses_db.py
├── docs/
│   └── USER_GUIDE.md               ← 使用指南 ★
├── examples/
│   ├── test-project-mit/
│   ├── test-project-gpl/
│   ├── test-project-apache/
│   ├── test-project-unclear/
│   └── test-project-no-license/
└── tests/                          ← 未來可以加測試