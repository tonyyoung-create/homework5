# 部署指南 - GitHub & Streamlit Cloud

## 第一步：準備本地環境

### 1. 安裝 Git
```bash
# Windows - 下載並安裝
https://git-scm.com/download/win

# macOS
brew install git

# Linux
sudo apt-get install git
```

### 2. 配置 Git
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 第二步：將專案推送到 GitHub

### 1. 在 GitHub 上建立新倉庫
- 訪問 https://github.com/new
- Repository name: `AI_Detection_System`
- Description: `Advanced AI Detection System based on Multi-dimensional Analysis`
- 選擇 Public (便於 Streamlit Cloud 訪問)
- 點擊 "Create repository"

### 2. 初始化本地 Git 倉庫
```bash
cd AI_Detection_System

# 初始化 git
git init

# 添加所有檔案
git add .

# 首次提交
git commit -m "Initial commit: AI Detection System v1.0"

# 添加遠端倉庫
git remote add origin https://github.com/YOUR_USERNAME/AI_Detection_System.git

# 推送到 GitHub (主分支)
git branch -M main
git push -u origin main
```

### 3. 驗證推送成功
- 訪問 https://github.com/YOUR_USERNAME/AI_Detection_System
- 確認所有檔案已上傳

## 第三步：在 Streamlit Cloud 部署

### 1. 註冊 Streamlit Cloud 帳戶
- 訪問 https://share.streamlit.io
- 點擊 "Sign up"
- 使用 GitHub 帳號登錄或建立新帳號

### 2. 部署應用
- 點擊 "New app"
- 選擇部署選項：
  - **GitHub Repo**: `YOUR_USERNAME/AI_Detection_System`
  - **Branch**: `main`
  - **Main file path**: `app.py`
- 點擊 "Deploy"

### 3. 等待部署完成
- Streamlit Cloud 會自動：
  - 克隆倉庫
  - 安裝 requirements.txt 中的依賴
  - 運行應用
- 應用 URL 會是：`https://share.streamlit.io/YOUR_USERNAME/ai-detection-system`

### 4. 首次運行的注意事項
- 首次運行可能需要 3-5 分鐘（下載模型）
- 建立訓練數據集（約 1-2 分鐘）
- 之後訪問速度會很快

## 第四步：配置和優化

### 1. 設置 Streamlit 配置
編輯 `.streamlit/config.toml`：
```toml
[client]
showErrorDetails = true

[server]
maxUploadSize = 200
```

### 2. 設置環境變數（如需要）
在 Streamlit Cloud 控制面板：
- 點擊應用設置
- 選擇 "Secrets"
- 添加所需的環境變數

### 3. 設置 Secrets (可選)
如果使用 API key，在 `.streamlit/secrets.toml` 添加：
```toml
[api]
key = "your-secret-key"
```

## 第五步：後續更新

### 推送更新到 GitHub
```bash
# 進行更改後
git add .
git commit -m "Update: Add new features"
git push origin main
```

Streamlit Cloud 會自動檢測更新並重新部署。

## 常見問題

### Q1: 模型文件太大怎麼辦？
**A**: 
- 不要上傳 `.pkl` 模型文件到 GitHub
- 在 Streamlit Cloud 上使用 `settings.py` 自動生成模型
- 或使用 Git LFS (Large File Storage)

### Q2: 我的應用超時了怎麼辦？
**A**:
- 首次訓練模型可能耗時，設置長超時
- 可以預先訓練模型並保存
- 使用較小的模型（如 DistilGPT-2）

### Q3: 如何查看運行日誌？
**A**:
- 在 Streamlit Cloud 控制面板選擇應用
- 點擊 "View logs"
- 查看實時日誌

### Q4: 我想使用自己的域名
**A**:
- Streamlit Cloud 不直接支持自定義域名
- 可以使用 Cloudflare 或其他 CDN 來配置代理

## 推薦的 GitHub 目錄結構

```
AI_Detection_System/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD 配置（可選）
├── .streamlit/
│   └── config.toml
├── utils/
│   ├── __init__.py
│   ├── feature_extractor.py
│   ├── data_manager.py
│   └── xai_visualizer.py
├── models/
│   ├── __init__.py
│   └── ai_detector.py
├── data/
│   ├── training_data_en.csv
│   └── training_data_cn.csv
├── .gitignore
├── app.py
├── flask_api.py
├── train.py
├── requirements.txt
├── README.md
└── DEPLOYMENT.md               # 本檔案
```

## 進階：使用 GitHub Actions 自動化

建立 `.github/workflows/ci.yml`：
```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Lint
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## 故障排除

### 應用無法啟動
1. 檢查 `requirements.txt` 中的依賴版本
2. 查看 Streamlit Cloud 日誌
3. 確保 `app.py` 在項目根目錄

### 模型未能載入
1. 確保模型文件在 `models/` 目錄
2. 檢查模型路徑是否正確
3. 考慮使用相對路徑而非絕對路徑

### 超時或記憶體不足
1. 使用較小的模型
2. 優化特徵提取速度
3. 使用快取（Streamlit 的 `@st.cache`）

## 監控和維護

### 定期檢查
- 日誌中的錯誤信息
- 應用使用統計
- 用戶反饋

### 性能優化建議
- 使用 `@st.cache_resource` 和 `@st.cache_data`
- 優化特徵提取算法
- 考慮使用更輕量的模型

## 獲取幫助

- Streamlit 文檔：https://docs.streamlit.io
- GitHub 幫助：https://docs.github.com
- 專案 Issue：在 GitHub repo 上提交 issue

---

**部署成功後，應用將在以下位置可用：**
```
https://share.streamlit.io/YOUR_USERNAME/ai-detection-system
```

享受您的 AI 偵測系統！🚀
