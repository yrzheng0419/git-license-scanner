#!/bin/bash
# 展示腳本 - 展示 Git License Scanner 的各種功能

echo "=========================================="
echo "🔍 Git License Scanner 功能展示"
echo "=========================================="
echo ""

echo "📌 測試 1: 掃描 MIT 授權專案"
echo "指令: license-scan examples/test-project-mit"
echo "------------------------------------------"
license-scan examples/test-project-mit
echo ""
read -p "按 Enter 繼續..."
echo ""

echo "📌 測試 2: 掃描 GPL 授權專案（高風險）"
echo "指令: license-scan examples/test-project-gpl -v"
echo "------------------------------------------"
license-scan examples/test-project-gpl -v
echo ""
read -p "按 Enter 繼續..."
echo ""

echo "📌 測試 3: 掃描模糊授權專案（低信心度警告）"
echo "指令: license-scan examples/test-project-unclear"
echo "------------------------------------------"
license-scan examples/test-project-unclear
echo ""
read -p "按 Enter 繼續..."
echo ""

echo "📌 測試 4: JSON 輸出"
echo "指令: license-scan . --output json"
echo "------------------------------------------"
license-scan . --output json
echo ""
read -p "按 Enter 繼續..."
echo ""

echo "=========================================="
echo "✅ 展示完成！"
echo "=========================================="