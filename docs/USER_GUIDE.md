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

### Q: 為什麼無法辨識授權？
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