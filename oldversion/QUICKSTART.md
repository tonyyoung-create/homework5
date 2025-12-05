# 快速開始指南 (Quick Start)

## 🚀 5分鐘快速啟動

### 前置條件
- Python 3.8+ 已安裝
- pip 已安裝

### 步驟 1: 複製專案
```bash
# 方式 1: 從 GitHub 克隆
git clone https://github.com/YOUR_USERNAME/AI_Detection_System.git
cd AI_Detection_System

# 方式 2: 直接下載 ZIP 檔案並解壓
```

### 步驟 2: 建立虛擬環境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 步驟 3: 安裝依賴
```bash
# 基本安裝（推薦）
pip install -r requirements.txt

# 或只安裝核心依賴（快速安裝）
pip install streamlit scikit-learn numpy pandas torch transformers nltk plotly
```

### 步驟 4: 下載 NLTK 資源（首次需要）
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('stopwords')"
```

### 步驟 5: 運行應用
```bash
streamlit run app.py
```

應用將在 `http://localhost:8501` 打開 🎉

## 📝 使用流程

### 第一次使用

1. **創建數據集**
   - 進入 "⚙️ Settings" 標籤
   - 點擊 "Create Sample Dataset" 按鈕
   - 等待完成

2. **訓練模型** (可選)
   - 在 "⚙️ Settings" 標籤
   - 點擊 "Train Model" 按鈕
   - 等待訓練完成（首次 5-10 分鐘）

3. **開始偵測**
   - 進入 "📝 Detection" 標籤
   - 粘貼或上傳文本
   - 點擊 "Analyze Text"
   - 查看結果！

### 快速測試文本

**AI 生成文本示例：**
```
Artificial intelligence represents a transformative technology 
that has revolutionized numerous industries. 
The implementation of machine learning algorithms enables systems 
to process and analyze vast amounts of data with unprecedented efficiency. 
Furthermore, deep learning approaches have demonstrated remarkable 
capabilities in tasks ranging from natural language processing to computer vision.
```

**Human 寫作示例：**
```
嗯天啦我真的超討厭這次的會議欸 
那傢伙一直在講些廢話 我差點睡著
最後還被老闆點名 我完全沒在聽 超尷尬
真的要改掉這個壞習慣啦😅
```

## 🔧 常用命令

```bash
# 激活虛擬環境
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# 退出虛擬環境
deactivate

# 線下訓練模型
python train.py

# 運行 Flask API 服務器
python flask_api.py

# 安裝新的依賴包
pip install <package_name>

# 更新依賴
pip install -r requirements.txt --upgrade

# 凍結當前環境
pip freeze > requirements.txt
```

## 📊 三種運行方式

### 方式 1: Streamlit Web UI (推薦)
```bash
streamlit run app.py
# URL: http://localhost:8501
```

### 方式 2: Flask REST API
```bash
python flask_api.py
# API URL: http://localhost:5000
# 文檔: http://localhost:5000/
```

### 方式 3: 命令行訓練
```bash
python train.py
# 訓練完成後模型保存到 models/ai_detector_model.pkl
```

## 🌐 部署到 Streamlit Cloud

### 準備工作
1. 推送到 GitHub
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. 訪問 https://share.streamlit.io

3. 連接 GitHub 並選擇該倉庫

4. 設定主檔案為 `app.py`

5. 部署！

詳細步驟見 [DEPLOYMENT.md](DEPLOYMENT.md)

## ⚙️ 配置調整

### 更改模型
編輯 `models/ai_detector.py`：
```python
# 改用其他語言模型
detector = AIDetector(model_name="gpt2")  # 預設是 distilgpt2
```

### 調整界面語言
在 `app.py` 中：
```python
language = st.sidebar.radio("語言", ["English", "中文"], index=1)  # 預設中文
```

### 修改應用色系
編輯 `.streamlit/config.toml`：
```toml
[theme]
primaryColor = "#FF4444"      # 主題色
backgroundColor = "#FFFFFF"   # 背景色
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"         # 文字顏色
font = "sans serif"
```

## 🐛 常見問題

### Q: 運行時出現 "ModuleNotFoundError"
**A**: 確保虛擬環境已激活，且已安裝所有依賴
```bash
pip install -r requirements.txt
```

### Q: 模型下載很慢
**A**: 首次下載語言模型 (~500MB) 需要時間，之後會快得多

### Q: 如何在 GPU 上運行？
**A**: 安裝 CUDA 版 PyTorch
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Q: 可以離線使用嗎？
**A**: 可以，但需要預先下載模型

### Q: 如何更新代碼？
**A**: 
```bash
git pull origin main
pip install -r requirements.txt --upgrade
streamlit run app.py
```

## 📚 進一步學習

- [Streamlit 文檔](https://docs.streamlit.io)
- [scikit-learn 文檔](https://scikit-learn.org)
- [Transformers 文檔](https://huggingface.co/docs/transformers)
- [理論參考](README.md)

## 🆘 需要幫助？

1. 查看 [README.md](README.md) 了解更多
2. 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 進行部署
3. 提交 GitHub Issue: https://github.com/YOUR_USERNAME/AI_Detection_System/issues

## 📱 下一步

完成快速啟動後，你可以：
- 📖 閱讀詳細的 README 文檔
- 🔬 深入理解理論基礎
- 🚀 部署到生產環境
- 🔧 自訂和擴展功能
- 📊 分析和改進模型

---

**享受使用 AI Detection System！** 🎉
