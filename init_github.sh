#!/bin/bash
# GitHub 初始化腳本 - macOS/Linux 版本

# 檢查 Git 是否已安裝
if ! command -v git &> /dev/null; then
    echo "Git 未安裝。請訪問 https://git-scm.com/download 下載並安裝。"
    exit 1
fi

echo "================================"
echo "AI Detection System - GitHub 初始化"
echo "================================"

# 第一步：初始化 Git 倉庫
echo ""
echo "✓ [步驟 1] 初始化本地 Git 倉庫..."
git init
if [ $? -ne 0 ]; then
    echo "✗ Git 初始化失敗"
    exit 1
fi
echo "✓ Git 倉庫已初始化"

# 第二步：配置 Git
echo ""
echo "✓ [步驟 2] 配置 Git 用戶信息..."
read -p "請輸入您的 GitHub 用戶名: " userName
read -p "請輸入您的 GitHub 郵箱: " userEmail
git config --global user.name "$userName"
git config --global user.email "$userEmail"
echo "✓ Git 用戶信息已設置"

# 第三步：添加遠端倉庫
echo ""
echo "✓ [步驟 3] 添加遠端倉庫..."
read -p "請輸入 GitHub 倉庫 URL (例如 https://github.com/username/AI_Detection_System.git): " githubUrl
git remote add origin "$githubUrl"
echo "✓ 遠端倉庫已添加"

# 第四步：添加所有檔案
echo ""
echo "✓ [步驟 4] 添加所有檔案..."
git add .
echo "✓ 所有檔案已添加"

# 第五步：首次提交
echo ""
echo "✓ [步驟 5] 創建首次提交..."
git commit -m "Initial commit: AI Detection System v1.0 - Complete implementation with Streamlit UI, feature extraction, and model training"
if [ $? -ne 0 ]; then
    echo "✗ 提交失敗"
    exit 1
fi
echo "✓ 首次提交已完成"

# 第六步：重命名分支為 main
echo ""
echo "✓ [步驟 6] 設置主分支為 main..."
git branch -M main
echo "✓ 分支已重命名為 main"

# 第七步：推送到 GitHub
echo ""
echo "✓ [步驟 7] 推送到 GitHub..."
echo "這將要求您輸入 GitHub 認證信息（或使用 Personal Access Token）"
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✓ GitHub 初始化完成！"
    echo "================================"
    echo ""
    echo "下一步："
    echo "1. 訪問 $githubUrl"
    echo "2. 驗證所有檔案已上傳"
    echo "3. 訪問 https://share.streamlit.io 部署應用"
    echo ""
    echo "詳細部署指南請查看 DEPLOYMENT.md"
else
    echo "✗ 推送到 GitHub 失敗，請檢查網絡連接和 GitHub URL"
    exit 1
fi
