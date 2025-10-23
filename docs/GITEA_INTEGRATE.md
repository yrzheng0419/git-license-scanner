# 🔗 與 Gitea 整合使用

雖然本工具是獨立的 CLI 工具，但可以輕鬆整合到 Gitea 工作流程中。以下是幾種整合方式：

---

## 方式 1：Git Hooks（推薦）

在 Gitea 儲存庫中設定 Git hooks，在推送程式碼前自動檢查授權。

### Pre-commit Hook（提交前檢查）

在儲存庫的 `.git/hooks/pre-commit` 建立以下腳本：

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 正在檢查授權合規性..."

# 執行授權掃描，輸出 JSON
license-scan . --output json --output-file /tmp/license-report.json

# 檢查是否有高風險授權
HIGH_RISK=$(jq '.summary.high_risk' /tmp/license-report.json)

if [ "$HIGH_RISK" -gt 0 ]; then
    echo "❌ 錯誤：發現 $HIGH_RISK 個高風險授權！"
    echo "請執行 'license-scan . -v' 查看詳情"
    exit 1
fi

echo "✅ 授權檢查通過"
exit 0
```

### Pre-push Hook（推送前檢查）

在 `.git/hooks/pre-push` 建立類似腳本：

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "🔍 推送前授權檢查..."

license-scan . --output json --output-file /tmp/license-report.json

HIGH_RISK=$(jq '.summary.high_risk' /tmp/license-report.json)
MEDIUM_RISK=$(jq '.summary.medium_risk' /tmp/license-report.json)

if [ "$HIGH_RISK" -gt 0 ]; then
    echo "❌ 阻止推送：發現高風險授權"
    license-scan . -v
    exit 1
fi

if [ "$MEDIUM_RISK" -gt 0 ]; then
    echo "⚠️  警告：發現中風險授權"
    read -p "是否繼續推送？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ 授權檢查通過"
exit 0
```

**使腳本可執行：**
```bash
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
```

---

## 方式 2：Gitea Webhooks + 自動掃描

當 Gitea 收到 push 事件時，觸發授權掃描。

### 設定步驟

#### 1. 建立掃描腳本

**位置：** `/opt/gitea-license-scanner.sh`

```bash
#!/bin/bash
# Gitea Webhook 掃描腳本

REPO_PATH=$1
REPO_NAME=$2

echo "掃描儲存庫: $REPO_NAME"

cd "$REPO_PATH"

# 執行掃描
license-scan . --output json --output-file "/var/log/gitea-license-reports/${REPO_NAME}.json"

# 檢查風險
HIGH_RISK=$(jq '.summary.high_risk' "/var/log/gitea-license-reports/${REPO_NAME}.json")

if [ "$HIGH_RISK" -gt 0 ]; then
    # 發送通知（可以整合 Slack, Email 等）
    echo "警告：$REPO_NAME 發現高風險授權" | mail -s "授權警告" admin@example.com
fi
```

#### 2. 在 Gitea 中設定 Webhook

- 進入儲存庫設定 → Webhooks
- URL: `http://your-server/webhook-handler`
- 選擇觸發事件：Push events

#### 3. 建立 Webhook 處理器

**簡單的 Python Flask 範例：**

```python
# webhook_handler.py
from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/webhook-handler', methods=['POST'])
def handle_webhook():
    data = request.json
    repo_name = data['repository']['name']
    repo_path = f"/var/gitea-repositories/{repo_name}"
    
    # 執行掃描腳本
    subprocess.run([
        '/opt/gitea-license-scanner.sh',
        repo_path,
        repo_name
    ])
    
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 方式 3：定期自動掃描所有儲存庫

使用 cron job 定期掃描 Gitea 上的所有儲存庫。

### 建立掃描腳本

**位置：** `/opt/scan-all-repos.sh`

```bash
#!/bin/bash
# 掃描所有 Gitea 儲存庫

GITEA_REPOS="/var/lib/gitea/repositories"
REPORT_DIR="/var/log/gitea-license-reports"
DATE=$(date +%Y%m%d)

mkdir -p "$REPORT_DIR/$DATE"

echo "開始掃描所有儲存庫..."

# 遍歷所有使用者的儲存庫
for user_dir in "$GITEA_REPOS"/*; do
    if [ -d "$user_dir" ]; then
        username=$(basename "$user_dir")
        
        for repo_dir in "$user_dir"/*.git; do
            if [ -d "$repo_dir" ]; then
                repo_name=$(basename "$repo_dir" .git)
                
                echo "掃描: $username/$repo_name"
                
                # 執行掃描
                license-scan "$repo_dir" \
                    --output json \
                    --output-file "$REPORT_DIR/$DATE/${username}_${repo_name}.json"
            fi
        done
    fi
done

# 產生摘要報告
echo "產生摘要報告..."
python3 /opt/generate-summary.py "$REPORT_DIR/$DATE"

echo "掃描完成！報告位於: $REPORT_DIR/$DATE"
```

### 摘要報告生成器

**位置：** `/opt/generate-summary.py`

```python
#!/usr/bin/env python3
# 產生所有掃描的摘要報告

import json
import sys
from pathlib import Path

def generate_summary(report_dir):
    reports_path = Path(report_dir)
    
    summary = {
        'total_repos': 0,
        'high_risk_repos': [],
        'medium_risk_repos': [],
        'low_risk_repos': [],
        'total_high_risk': 0,
        'total_medium_risk': 0,
        'total_low_risk': 0,
    }
    
    for report_file in reports_path.glob('*.json'):
        with open(report_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        summary['total_repos'] += 1
        repo_name = report_file.stem
        
        high = data['summary']['high_risk']
        medium = data['summary']['medium_risk']
        low = data['summary']['low_risk']
        
        summary['total_high_risk'] += high
        summary['total_medium_risk'] += medium
        summary['total_low_risk'] += low
        
        if high > 0:
            summary['high_risk_repos'].append(repo_name)
        elif medium > 0:
            summary['medium_risk_repos'].append(repo_name)
        else:
            summary['low_risk_repos'].append(repo_name)
    
    # 輸出摘要
    print("\n" + "="*60)
    print("Gitea 授權掃描摘要報告")
    print("="*60)
    print(f"總儲存庫數: {summary['total_repos']}")
    print(f"高風險授權數: {summary['total_high_risk']}")
    print(f"中風險授權數: {summary['total_medium_risk']}")
    print(f"低風險授權數: {summary['total_low_risk']}")
    print()
    
    if summary['high_risk_repos']:
        print("⚠️  高風險儲存庫:")
        for repo in summary['high_risk_repos']:
            print(f"  - {repo}")
    
    if summary['medium_risk_repos']:
        print("\n⚠️  中風險儲存庫:")
        for repo in summary['medium_risk_repos']:
            print(f"  - {repo}")
    
    # 儲存 JSON 摘要
    summary_file = reports_path / 'summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n摘要已儲存至: {summary_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("使用方式: python3 generate-summary.py <report_directory>")
        sys.exit(1)
    
    generate_summary(sys.argv[1])
```

### 設定 Cron Job

```bash
# 編輯 crontab
crontab -e

# 每天凌晨 2 點執行
0 2 * * * /opt/scan-all-repos.sh >> /var/log/gitea-license-scan.log 2>&1

# 每週一上午 9 點執行
0 9 * * 1 /opt/scan-all-repos.sh >> /var/log/gitea-license-scan.log 2>&1
```

---

## 方式 4：Gitea Actions（CI/CD 整合）

在 Gitea Actions 工作流程中加入授權檢查。

### 配置檔案

**位置：** `.gitea/workflows/license-check.yml`

```yaml
name: License Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  license-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install license-scanner
      run: |
        pip install git+https://github.com/yourusername/git-license-scanner.git
    
    - name: Scan licenses
      run: |
        license-scan . --output json --output-file license-report.json
    
    - name: Check for high-risk licenses
      run: |
        HIGH_RISK=$(jq '.summary.high_risk' license-report.json)
        if [ "$HIGH_RISK" -gt 0 ]; then
          echo "❌ 發現高風險授權！"
          license-scan . -v
          exit 1
        fi
        echo "✅ 授權檢查通過"
    
    - name: Upload report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: license-report
        path: license-report.json
```

---

## 方式 5：手動掃描特定 Gitea 儲存庫

如果你的 Gitea 儲存庫在本機，可以直接掃描：

```bash
# 掃描特定儲存庫
license-scan /var/lib/gitea/repositories/username/repo.git

# 掃描所有某個使用者的儲存庫
for repo in /var/lib/gitea/repositories/username/*.git; do
    echo "掃描: $repo"
    license-scan "$repo" -v
done

# 批次掃描並產生報告
for repo in /var/lib/gitea/repositories/*/*.git; do
    repo_name=$(basename "$(dirname "$repo")")/$(basename "$repo" .git)
    license-scan "$repo" --output json --output-file "reports/${repo_name}.json"
done
```

---

## 整合效益

✅ **自動化合規檢查**：不需人工審查每個授權  
✅ **即時風險預警**：在問題進入主分支前發現  
✅ **審計追蹤**：保留所有掃描記錄供稽核  
✅ **團隊通知**：透過 webhook 通知相關人員  
✅ **持續監控**：定期掃描確保長期合規  

---

## 進階：與 Gitea API 整合

使用 Gitea API 自動化管理：

```python
#!/usr/bin/env python3
# gitea_license_monitor.py

import requests
import subprocess
import json

GITEA_URL = "http://localhost:3000"
GITEA_TOKEN = "your-gitea-token"

def get_all_repos():
    """取得所有儲存庫"""
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    response = requests.get(f"{GITEA_URL}/api/v1/repos/search", headers=headers)
    return response.json()['data']

def scan_repo(repo_name, clone_url):
    """掃描儲存庫"""
    # Clone 儲存庫
    subprocess.run(['git', 'clone', clone_url, f'/tmp/{repo_name}'])
    
    # 掃描
    result = subprocess.run(
        ['license-scan', f'/tmp/{repo_name}', '--output', 'json'],
        capture_output=True,
        text=True
    )
    
    return json.loads(result.stdout)

def create_issue_if_high_risk(repo, scan_result):
    """如果發現高風險授權，自動建立 issue"""
    if scan_result['summary']['high_risk'] > 0:
        headers = {
            "Authorization": f"token {GITEA_TOKEN}",
            "Content-Type": "application/json"
        }
        
        issue_data = {
            "title": "⚠️ 發現高風險授權",
            "body": f"""
自動授權掃描發現高風險授權：

- 高風險授權數: {scan_result['summary']['high_risk']}
- 中風險授權數: {scan_result['summary']['medium_risk']}

請檢查並處理這些授權問題。

詳細報告請執行: `license-scan . -v`
            """,
            "labels": ["security", "license"]
        }
        
        requests.post(
            f"{GITEA_URL}/api/v1/repos/{repo['full_name']}/issues",
            headers=headers,
            json=issue_data
        )

if __name__ == '__main__':
    repos = get_all_repos()
    
    for repo in repos:
        print(f"掃描: {repo['full_name']}")
        scan_result = scan_repo(repo['name'], repo['clone_url'])
        create_issue_if_high_risk(repo, scan_result)
```

執行定期監控：
```bash
# 每天執行一次
0 0 * * * /usr/bin/python3 /opt/gitea_license_monitor.py
```

---

## 範例：完整的 Gitea 整合架構

```
┌─────────────────────────────────────────────────────────┐
│                      Gitea Server                        │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │  Repo A    │  │  Repo B    │  │  Repo C    │       │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘       │
│        │                │                │              │
│        └────────────────┴────────────────┘              │
│                         │                               │
└─────────────────────────┼───────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   Git Hooks / CI/CD   │
              │  license-scan tool    │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   授權風險評估         │
              └───────────┬───────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    ┌─────────┐    ┌──────────┐    ┌─────────┐
    │ 通知團隊 │    │ 建立Issue │    │ 產生報告 │
    └─────────┘    └──────────┘    └─────────┘
```

---

## 實際使用案例

### 案例 1：新創公司的合規檢查

**情境：** 開發團隊有 10+ 個專案，需要在融資前進行授權合規檢查

**解決方案：**
```bash
# 掃描所有專案
for repo in /var/lib/gitea/repositories/startup/*; do
    license-scan "$repo" --output json --output-file "reports/$(basename $repo).json"
done

# 產生合規報告給投資者
python3 generate-summary.py reports/
```

### 案例 2：開源專案維護者

**情境：** 確保所有貢獻者的 PR 不會引入不相容的授權

**解決方案：**
- 設定 pre-push hook
- 整合到 CI/CD pipeline
- 自動在 PR 中顯示授權掃描結果

### 案例 3：企業合規稽核

**情境：** 每季度需要向法務部門提供授權合規報告

**解決方案：**
```bash
# 每季度自動執行
0 0 1 */3 * /opt/scan-all-repos.sh && \
  python3 /opt/generate-compliance-report.py >> /var/reports/quarterly-report.pdf
```

---

## 常見問題

### Q1: Git hooks 在團隊中如何共享？

**A:** 可以將 hooks 放在版本控制中：

```bash
# 在專案根目錄建立
mkdir .githooks

# 將 hook 放入
cp .git/hooks/pre-commit .githooks/

# 設定 Git 使用自訂 hooks 目錄
git config core.hooksPath .githooks

# 團隊成員 clone 後執行
git config core.hooksPath .githooks
```

### Q2: 如何處理誤報？

**A:** 可以建立白名單配置：

```yaml
# license-scan-config.yml
ignore_paths:
  - vendor/
  - node_modules/
  
trusted_licenses:
  - MIT
  - Apache-2.0
  - BSD-3-Clause
```

### Q3: 大型儲存庫掃描很慢怎麼辦？

**A:** 可以只掃描變更的檔案：

```bash
# 只掃描最近的 commit
git diff-tree --no-commit-id --name-only -r HEAD | \
  while read file; do
    if [[ "$file" == "LICENSE"* ]]; then
      license-scan "$file"
    fi
  done
```

---

## 延伸閱讀

- [Gitea Webhooks 文件](https://docs.gitea.io/en-us/webhooks/)
- [Git Hooks 官方文件](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [開源授權合規最佳實踐](https://opensource.guide/legal/)

---

## 總結

透過這些整合方式，Git License Scanner 可以：

✅ 無縫整合到現有的 Gitea 工作流程  
✅ 提供多層次的授權檢查（本地、推送、CI/CD）  
✅ 自動化合規報告生成  
✅ 即時風險預警與團隊通知  
✅ 支援從小型團隊到大型企業的不同需求  

選擇最適合你團隊的整合方式，開始自動化授權管理吧！