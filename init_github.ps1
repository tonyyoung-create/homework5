#!/bin/bash
# GitHub 初始化腳本 - Windows PowerShell 版本

# 檢查 Git 是否已安裝
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git 未安裝。請訪問 https://git-scm.com/download/win 下載並安裝。"
    Exit 1
}

Write-Host "================================" -ForegroundColor Green
Write-Host "AI Detection System - GitHub 初始化" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# 第一步：初始化 Git 倉庫
Write-Host "`n[步驟 1] 初始化本地 Git 倉庫..." -ForegroundColor Cyan
git init
if ($LASTEXITCODE -ne 0) {
    Write-Error "Git 初始化失敗"
    Exit 1
}
Write-Host "✓ Git 倉庫已初始化" -ForegroundColor Green

# 第二步：配置 Git
Write-Host "`n[步驟 2] 配置 Git 用戶信息..." -ForegroundColor Cyan
$userName = Read-Host "請輸入您的 GitHub 用戶名"
$userEmail = Read-Host "請輸入您的 GitHub 郵箱"
git config --global user.name "$userName"
git config --global user.email "$userEmail"
Write-Host "✓ Git 用戶信息已設置" -ForegroundColor Green

# 第三步：添加遠端倉庫
Write-Host "`n[步驟 3] 添加遠端倉庫..." -ForegroundColor Cyan
$githubUrl = Read-Host "請輸入 GitHub 倉庫 URL (例如 https://github.com/username/AI_Detection_System.git)"
git remote add origin "$githubUrl"
Write-Host "✓ 遠端倉庫已添加" -ForegroundColor Green

# 第四步：添加所有檔案
Write-Host "`n[步驟 4] 添加所有檔案..." -ForegroundColor Cyan
git add .
Write-Host "✓ 所有檔案已添加" -ForegroundColor Green

# 第五步：首次提交
Write-Host "`n[步驟 5] 創建首次提交..." -ForegroundColor Cyan
git commit -m "Initial commit: AI Detection System v1.0 - Complete implementation with Streamlit UI, feature extraction, and model training"
if ($LASTEXITCODE -ne 0) {
    Write-Error "提交失敗"
    Exit 1
}
Write-Host "✓ 首次提交已完成" -ForegroundColor Green

# 第六步：重命名分支為 main
Write-Host "`n[步驟 6] 設置主分支為 main..." -ForegroundColor Cyan
git branch -M main
Write-Host "✓ 分支已重命名為 main" -ForegroundColor Green

# 第七步：推送到 GitHub
Write-Host "`n[步驟 7] 推送到 GitHub..." -ForegroundColor Cyan
Write-Host "這將要求您輸入 GitHub 認證信息（或使用 Personal Access Token）" -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n================================" -ForegroundColor Green
    Write-Host "✓ GitHub 初始化完成！" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host "`n下一步：" -ForegroundColor Cyan
    Write-Host "1. 訪問 $githubUrl" -ForegroundColor White
    Write-Host "2. 驗證所有檔案已上傳" -ForegroundColor White
    Write-Host "3. 訪問 https://share.streamlit.io 部署應用" -ForegroundColor White
    Write-Host "`n詳細部署指南請查看 DEPLOYMENT.md" -ForegroundColor Cyan
} else {
    Write-Error "推送到 GitHub 失敗，請檢查網絡連接和 GitHub URL"
    Exit 1
}
