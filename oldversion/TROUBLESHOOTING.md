# 測試與故障排除指南

## 🧪 測試流程

### 第一階段：環境測試

#### 1. 檢查 Python 版本
```bash
python --version
# 應該是 3.8 或更高版本
```

#### 2. 檢查虛擬環境
```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 檢查 pip
pip --version
```

#### 3. 檢查依賴安裝
```bash
pip list
# 確保列出了 streamlit, torch, transformers 等

# 或檢查特定包
pip show streamlit
```

### 第二階段：模組測試

#### 1. 測試特徵提取
```bash
python -c "
from utils.feature_extractor import FeatureExtractor
extractor = FeatureExtractor()
text = 'This is a test text.'
features = extractor.extract_all_features(text)
print(f'✓ Extracted {len(features)} features')
print(features)
"
```

#### 2. 測試數據管理
```bash
python -c "
from utils.data_manager import create_dataset, load_dataset
create_dataset('data/test_data.csv', language='english')
data = load_dataset('data/test_data.csv')
print(f'✓ Loaded {len(data)} samples')
"
```

#### 3. 測試分類器
```bash
python -c "
from models.ai_detector import AIDetector
detector = AIDetector()
print('✓ Detector initialized successfully')
"
```

#### 4. 測試 XAI 可視化
```bash
python -c "
from utils.xai_visualizer import XAIVisualizer
visualizer = XAIVisualizer()
print('✓ Visualizer initialized successfully')
"
```

### 第三階段：集成測試

#### 1. 運行訓練腳本
```bash
python train.py
# 應該看到訓練進度和最終結果
```

#### 2. 運行 Streamlit 應用
```bash
streamlit run app.py
# 應該在 http://localhost:8501 打開
```

#### 3. 運行 Flask API
```bash
python flask_api.py
# 應該在 http://localhost:5000 啟動
```

## 🐛 常見問題和解決方案

### 問題 1: ModuleNotFoundError 或 ImportError

**症狀**:
```
ModuleNotFoundError: No module named 'streamlit'
```

**解決方案**:
```bash
# 確保虛擬環境已激活
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 重新安裝依賴
pip install -r requirements.txt

# 或單獨安裝缺失的模組
pip install streamlit
```

### 問題 2: NLTK 資源缺失

**症狀**:
```
LookupError: Resource punkt not found
```

**解決方案**:
```bash
python -m nltk.downloader punkt averaged_perceptron_tagger stopwords
```

### 問題 3: CUDA / GPU 不可用

**症狀**:
```
torch.cuda.is_available() returns False
```

**解決方案**:
```bash
# 檢查 PyTorch CUDA 版本
python -c "import torch; print(torch.cuda.is_available())"

# 如果需要 GPU 支持，重新安裝 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 或使用 CPU 版本 (更簡單)
pip install torch torchvision torchaudio
```

### 問題 4: 模型下載超時

**症狀**:
```
ConnectionError: Connection timeout when downloading model
```

**解決方案**:
```bash
# 手動指定模型快取目錄
set HF_HOME=C:\path\to\cache  # Windows
export HF_HOME=/path/to/cache  # macOS/Linux

# 使用較小的模型
# 編輯 utils/feature_extractor.py，改為 "distilgpt2"
```

### 問題 5: 記憶體不足

**症狀**:
```
RuntimeError: CUDA out of memory
```

**解決方案**:
```python
# 編輯 utils/feature_extractor.py
# 改用 CPU 而非 GPU
device = torch.device('cpu')  # 強制使用 CPU

# 或減小批量大小
```

### 問題 6: Streamlit 應用不加載

**症狀**:
```
Error: list index out of range
或其他 Streamlit 特定錯誤
```

**解決方案**:
```bash
# 清除 Streamlit 快取
streamlit cache clear

# 重新運行
streamlit run app.py --logger.level=debug

# 檢查 .streamlit/config.toml 配置
```

### 問題 7: Git 推送認證失敗

**症狀**:
```
fatal: Authentication failed
```

**解決方案**:

**方法 A: 使用 Personal Access Token (推薦)**
```bash
# 1. 在 GitHub 生成 Personal Access Token
# 2. 當要求密碼時，粘貼 token 而非密碼

# 3. 或配置 Git 記住憑證
git config --global credential.helper store
git push origin main
# 第一次會要求輸入，之後會記住
```

**方法 B: 使用 SSH Key**
```bash
# 1. 生成 SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# 2. 將公鑰添加到 GitHub

# 3. 修改遠端 URL 為 SSH
git remote set-url origin git@github.com:USERNAME/AI_Detection_System.git

# 4. 推送
git push origin main
```

## ✅ 快速診斷檢查清單

```bash
#!/bin/bash
echo "AI Detection System - 診斷檢查"
echo "================================"

# 1. Python
echo -n "✓ Python 版本: "
python --version

# 2. 虛擬環境
echo -n "✓ 虛擬環境: "
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "已激活"
else
    echo "未激活"
fi

# 3. 關鍵依賴
echo "✓ 關鍵依賴:"
for package in streamlit numpy pandas torch transformers scikit-learn plotly; do
    python -c "import $package; print(f'  - $package: ✓')" 2>/dev/null || echo "  - $package: ✗"
done

# 4. NLTK 資源
echo -n "✓ NLTK 資源: "
python -c "import nltk; nltk.data.find('tokenizers/punkt'); print('✓')" 2>/dev/null || echo "✗ (運行: python -m nltk.downloader punkt)"

# 5. 模型檔案
echo -n "✓ 模型檔案: "
if [ -f "models/ai_detector_model.pkl" ]; then
    echo "✓"
else
    echo "✗ (需要訓練)"
fi

# 6. 數據檔案
echo -n "✓ 數據檔案: "
if [ -f "data/training_data_en.csv" ]; then
    echo "✓"
else
    echo "✗ (需要生成)"
fi

echo ""
echo "================================"
echo "診斷完成！"
```

## 📋 預部署檢查清單

在部署到 Streamlit Cloud 之前：

- [ ] 所有依賴項已在 `requirements.txt` 中列出
- [ ] `.gitignore` 已正確配置（排除模型文件）
- [ ] `.streamlit/config.toml` 已配置
- [ ] `app.py` 在項目根目錄
- [ ] 沒有硬編碼的絕對路徑
- [ ] 所有導入語句都正確
- [ ] 沒有本地文件依賴（除了數據集）
- [ ] 代碼可以在沒有 GPU 的情況下運行
- [ ] 已測試文本輸入和分析功能
- [ ] 所有文件已 git add 並提交
- [ ] 已推送到 GitHub

## 🔍 詳細日誌調試

### 啟用詳細日誌
```bash
# Streamlit
streamlit run app.py --logger.level=debug

# Python 日誌
export PYTHONUNBUFFERED=1
python train.py 2>&1 | tee debug.log
```

### 檢查模型加載
```python
import sys
sys.path.insert(0, '.')

from models.ai_detector import AIDetector

try:
    detector = AIDetector(model_path='models/ai_detector_model.pkl')
    print("✓ 模型加載成功")
    print(f"  - 特徵數: {len(detector.feature_names)}")
    print(f"  - 模型類型: {type(detector.classifier)}")
except Exception as e:
    print(f"✗ 模型加載失敗: {e}")
    import traceback
    traceback.print_exc()
```

## 📞 獲取幫助

如果問題無法解決：

1. 查看 [README.md](README.md) 中的詳細文檔
2. 查看 [QUICKSTART.md](QUICKSTART.md) 中的快速開始
3. 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 中的部署指南
4. 在 GitHub 上提交 Issue
5. 查看 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 了解完整項目概況

---

**最後更新**: 2024 年  
**版本**: 1.0.0
