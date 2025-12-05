# 🌐 完整雲端部署指南

完全在雲端執行 AI Detection System，支持 Streamlit Cloud

## 📋 快速部署（5分鐘）

### 方法 1️⃣: Streamlit Cloud（推薦 - 最簡單）

#### 步驟 1: 準備 GitHub 倉庫

```bash
# 1. 在 GitHub 上建立新倉庫
# 訪問 https://github.com/new
# 倉庫名稱: ai-detection-system
# 描述: Advanced AI-Generated Text Detection
# Public 公開倉庫
```

#### 步驟 2: 推送代碼到 GitHub

```bash
# 在項目目錄中執行
cd AI_Detection_System

# 初始化 Git
git init
git add .
git commit -m "Initial commit: AI Detection System v1.0"

# 添加遠程倉庫
git remote add origin https://github.com/YOUR_USERNAME/ai-detection-system.git
git branch -M main
git push -u origin main
```

#### 步驟 3: 在 Streamlit Cloud 上部署

1. **訪問** https://streamlit.io/cloud
2. **點擊** "New app"
3. **選擇**:
   - Repository: `YOUR_USERNAME/ai-detection-system`
   - Branch: `main`
   - Main file path: `app.py`
4. **點擊** "Deploy"

✅ **完成！** 應用將在 5-10 分鐘內上線

應用 URL 將是: `https://[project-name].streamlit.app`

---

### 方法 2️⃣: Heroku（需要信用卡）

#### 前置要求
- Heroku 帳戶: https://www.heroku.com
- Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

#### 部署步驟

```bash
# 1. 登入 Heroku
heroku login

# 2. 建立應用
heroku create ai-detection-system

# 3. 推送代碼
git push heroku main

# 4. 查看日誌
heroku logs --tail
```

應用 URL: `https://ai-detection-system.herokuapp.com`

---

### 方法 3️⃣: AWS (使用 EC2)

#### 前置要求
- AWS 帳戶
- EC2 實例 (Ubuntu 20.04 或更新)
- SSH 訪問

#### 部署步驟

```bash
# 1. SSH 連接到 EC2 實例
ssh -i your-key.pem ec2-user@your-instance-ip

# 2. 安裝依賴
sudo apt update
sudo apt install python3-pip git -y

# 3. 克隆倉庫
git clone https://github.com/YOUR_USERNAME/ai-detection-system.git
cd ai-detection-system

# 4. 安裝 Python 依賴
pip install -r requirements.txt

# 5. 配置 Streamlit（守護進程模式）
mkdir -p ~/.streamlit
cat > ~/.streamlit/config.toml << EOF
[server]
headless = true
port = 8501
[logger]
level = "info"
EOF

# 6. 啟動應用（背景運行）
nohup streamlit run app.py --server.address 0.0.0.0 > app.log 2>&1 &

# 7. 配置防火牆
sudo ufw allow 8501

# 查看應用
# 訪問: http://your-instance-ip:8501
```

---

## ⚙️ 環境變量配置

### Streamlit Cloud 環境變量設置

在 Streamlit Cloud 儀表板中設置（如需要）:

```
PYTHONPATH=.
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
```

### 本地環境文件 (.env)

如果需要敏感信息（暫不需要）:

```bash
# 創建 .env 文件
touch .env

# 添加內容
cat > .env << EOF
# API Keys (if needed in future)
# API_KEY=your_key_here
EOF

# 在代碼中讀取
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')
```

---

## 📦 部署前檢查清單

- [ ] 所有依賴都在 `requirements.txt` 中
- [ ] 沒有本地路徑（使用相對路徑）
- [ ] 沒有硬編碼敏感信息
- [ ] `app.py` 是主文件
- [ ] `.gitignore` 配置正確
- [ ] README.md 包含使用說明
- [ ] Git 已初始化並推送到 GitHub

檢查清單腳本:

```bash
# 檢查依賴
cat requirements.txt | sort

# 檢查本地路徑
grep -r "C:\\" . --include="*.py" | grep -v ".git"

# 檢查敏感信息
grep -r "password\|secret\|key\|token" . --include="*.py" | grep -v ".git"

# 檢查 .gitignore
cat .gitignore
```

---

## 🚀 部署後測試

### 1. 訪問應用

```
https://your-app.streamlit.app
```

### 2. 測試功能

- [ ] 文本輸入工作
- [ ] 分析按鈕響應
- [ ] AI 判別邏輯正確
- [ ] 特徵顯示完整
- [ ] 分析標籤有效
- [ ] 設置標籤工作

### 3. 檢查日誌

**Streamlit Cloud:**
- 登入 Streamlit Cloud
- 進入應用管理面板
- 查看 "Logs" 標籤

**Heroku:**
```bash
heroku logs --tail --app ai-detection-system
```

**AWS EC2:**
```bash
tail -f app.log
```

---

## 🔧 常見問題解決

### 問題 1: 應用加載緩慢

**原因**: 模型下載或特徵提取耗時

**解決**:
```python
# 在 app.py 中添加快取
@st.cache_resource
def load_feature_extractor():
    return FeatureExtractor()

@st.cache_resource
def load_detector():
    return AIDetector()
```

### 問題 2: NLTK 數據缺失

**錯誤**:
```
Resource punkt_tab not found
```

**解決**: 在 `requirements.txt` 後添加初始化腳本

創建 `setup_nltk.py`:
```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
```

在 Streamlit Cloud 部署時，添加到 `~/.streamlit/config.toml`:

```toml
[client]
runOnSave = true

[logger]
level = "info"
```

### 問題 3: 內存不足

**原因**: 模型文件太大

**解決**: 使用 DistilGPT-2 而不是 GPT-2（已默認配置）

### 問題 4: 超時錯誤

**原因**: 分析耗時過長

**解決**: 添加超時邏輯

```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Analysis timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 秒超時

try:
    # 分析代碼
    pass
finally:
    signal.alarm(0)
```

---

## 📊 監控和維護

### 使用情況監控

**Streamlit Cloud 儀表板:**
- 應用運行時間
- 用戶會話數
- 資源使用情況

### 日誌監控

**設置日誌通知** (可選):

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 在應用中使用
logger.info("Text analysis started")
logger.warning("Feature extraction warning")
logger.error("Critical error occurred")
```

### 性能優化

1. **缓存特徵提取器**:
```python
@st.cache_resource
def get_feature_extractor():
    return FeatureExtractor()
```

2. **缓存模型加載**:
```python
@st.cache_resource
def get_detector():
    return AIDetector(model_path="models/ai_detector_model.pkl")
```

3. **優化文本預處理**:
```python
# 只提取前 1000 個單詞進行快速分析
text_sample = text[:5000]
features = extractor.extract_all_features(text_sample)
```

---

## 🔐 安全建議

### 1. 環境變量管理

```bash
# 不要提交 .env 文件
echo ".env" >> .gitignore

# 在 Streamlit Cloud 上設置敏感數據
# 進入應用設置 > Secrets
# 添加密鑰到 secrets.toml
```

### 2. 限制請求

```python
# 添加速率限制
from datetime import datetime, timedelta

request_times = []

def check_rate_limit():
    now = datetime.now()
    # 移除超過 1 小時的請求
    request_times[:] = [t for t in request_times if now - t < timedelta(hours=1)]
    
    if len(request_times) > 100:
        st.error("Rate limit exceeded")
        return False
    
    request_times.append(now)
    return True
```

### 3. 輸入驗證

```python
import re

def validate_text(text):
    # 限制文本長度
    if len(text) > 100000:
        st.error("Text too long (max 100k chars)")
        return False
    
    # 檢查有效字符
    if not re.match(r'^[\w\s\.,!?-]+$', text, re.UNICODE):
        st.warning("Text contains unusual characters")
    
    return True
```

---

## 📈 擴展性建議

### 多區域部署

```bash
# 使用 CloudFlare 進行全球加速
# 1. 訪問 https://www.cloudflare.com
# 2. 添加自定義域名
# 3. 配置 DNS 指向 Streamlit 應用
```

### 負載均衡

```bash
# 使用 AWS Load Balancer
# 1. 創建多個 EC2 實例
# 2. 配置 Application Load Balancer
# 3. 自動伸縮組
```

### 數據庫集成 (未來)

```python
# 如需保存用戶歷史
import sqlite3

def save_analysis_history(text, result, user_id):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('INSERT INTO analyses VALUES (?, ?, ?, ?)',
              (user_id, text[:100], result, datetime.now()))
    conn.commit()
    conn.close()
```

---

## 🎯 完整部署檢查清單

### 準備階段
- [ ] 代碼已審查
- [ ] 所有測試通過
- [ ] 依賴已更新
- [ ] 文檔已完成
- [ ] README 已更新

### GitHub 準備
- [ ] 倉庫已建立
- [ ] 代碼已推送
- [ ] .gitignore 正確
- [ ] README.md 完整
- [ ] requirements.txt 準確

### 雲端部署
- [ ] 平台帳戶已建立
- [ ] 環境變量已設置
- [ ] 應用已部署
- [ ] 日誌已檢查
- [ ] 功能已測試

### 部署後
- [ ] 應用 URL 已記錄
- [ ] 用戶已通知
- [ ] 監控已啟用
- [ ] 備份已配置
- [ ] 文檔已更新

---

## 📞 獲取幫助

### Streamlit 支持
- **文檔**: https://docs.streamlit.io
- **論壇**: https://discuss.streamlit.io
- **GitHub Issues**: https://github.com/streamlit/streamlit/issues

### 部署平台
- **Streamlit Cloud**: https://docs.streamlit.io/streamlit-cloud
- **Heroku**: https://devcenter.heroku.com/articles/getting-started-with-python
- **AWS**: https://aws.amazon.com/getting-started

### 項目支持
- **GitHub**: [Your Repo URL]
- **Email**: [Contact Email]
- **Issues**: [GitHub Issues URL]

---

## 🎉 成功信號

應用已成功部署，當您看到：

✅ 應用 URL 可訪問
✅ "Streamlit app is running" 信息
✅ 文本輸入框出現
✅ 分析按鈕可點擊
✅ 結果顯示正確的 AI 判別

---

**祝賀！🎊 您的 AI Detection System 已上線！**

現在可以分享應用鏈接，讓任何人在雲端使用。

---

**最後更新**: 2024-12-05
**版本**: 1.0
**狀態**: ✅ 準備就緒
