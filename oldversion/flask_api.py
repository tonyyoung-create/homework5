"""
Flask API 版本 - 提供 REST API 端點
可選替代 Streamlit 的選擇
"""

from flask import Flask, request, jsonify, render_template_string
import sys
from pathlib import Path
import json

# 添加專案路徑
sys.path.insert(0, str(Path(__file__).parent))

from utils.feature_extractor import FeatureExtractor
from models.ai_detector import AIDetector

app = Flask(__name__)

# 全局變量
detector = None
feature_extractor = None


def initialize():
    """初始化模型"""
    global detector, feature_extractor
    
    try:
        detector = AIDetector(model_path='models/ai_detector_model.pkl')
    except:
        detector = AIDetector()
    
    feature_extractor = FeatureExtractor()


# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Detection API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.95rem;
        }
        .api-section {
            margin: 30px 0;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .api-section h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.1rem;
        }
        .endpoint {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
        .method {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            color: white;
            font-weight: bold;
            margin-right: 10px;
            font-size: 0.85rem;
        }
        .method.post { background: #4CAF50; }
        .method.get { background: #2196F3; }
        .example {
            background: #f9f9f9;
            padding: 15px;
            margin: 15px 0;
            border-left: 3px solid #ddd;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s;
        }
        button:hover { background: #764ba2; }
        textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            resize: vertical;
            min-height: 100px;
        }
        .response {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
            margin-top: 15px;
            display: none;
        }
        .response.show { display: block; }
        .response pre {
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
        }
        footer {
            text-align: center;
            color: #999;
            margin-top: 40px;
            font-size: 0.9rem;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Detection System - API</h1>
        <p class="subtitle">REST API for detecting AI-generated text</p>

        <div class="api-section">
            <h3>📝 Quick Test</h3>
            <textarea id="testText" placeholder="Enter text to analyze..."></textarea>
            <button onclick="testAPI()">Analyze</button>
            <div id="response" class="response">
                <pre id="responseText"></pre>
            </div>
        </div>

        <div class="api-section">
            <h3>📚 API Documentation</h3>
            
            <div class="endpoint">
                <span class="method post">POST</span> <strong>/api/predict</strong>
                <p style="margin-top: 10px; color: #666;">Analyze text and get AI probability</p>
                <div class="example">
curl -X POST http://localhost:5000/api/predict \\
  -H "Content-Type: application/json" \\
  -d '{"text": "Your text here..."}'
                </div>
                <p style="color: #666; margin-top: 10px;"><strong>Response:</strong></p>
                <div class="example">
{
  "prediction": 1,
  "ai_probability": 0.85,
  "human_probability": 0.15,
  "confidence": 0.85,
  "top_features": [...]
}
                </div>
            </div>

            <div class="endpoint">
                <span class="method post">POST</span> <strong>/api/features</strong>
                <p style="margin-top: 10px; color: #666;">Extract features only</p>
                <div class="example">
curl -X POST http://localhost:5000/api/features \\
  -H "Content-Type: application/json" \\
  -d '{"text": "Your text here..."}'
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span> <strong>/api/health</strong>
                <p style="margin-top: 10px; color: #666;">Check API health status</p>
            </div>
        </div>

        <footer>
            <p>AI Detection System v1.0 | Flask API Server</p>
            <p>Base URL: http://localhost:5000</p>
        </footer>
    </div>

    <script>
        function testAPI() {
            const text = document.getElementById('testText').value;
            if (!text.trim()) {
                alert('Please enter text to analyze');
                return;
            }

            fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({text: text})
            })
            .then(response => response.json())
            .then(data => {
                const response = document.getElementById('response');
                const responseText = document.getElementById('responseText');
                responseText.textContent = JSON.stringify(data, null, 2);
                response.classList.add('show');
            })
            .catch(error => {
                alert('Error: ' + error);
            });
        }
    </script>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    """主頁面"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/health', methods=['GET'])
def health():
    """健康檢查"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': detector is not None and detector.classifier is not None,
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """預測文本"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        if detector and detector.classifier:
            result = detector.predict(text)
        else:
            # 如果沒有訓練的模型，只進行特徵分析
            features = feature_extractor.extract_all_features(text)
            result = {
                'prediction': None,
                'ai_probability': None,
                'human_probability': None,
                'confidence': None,
                'extracted_features': features,
            }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/features', methods=['POST'])
def extract_features():
    """只提取特徵"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        features = feature_extractor.extract_all_features(text)
        
        return jsonify({
            'features': features,
            'num_features': len(features),
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch', methods=['POST'])
def batch_predict():
    """批量預測"""
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts or not isinstance(texts, list):
            return jsonify({'error': 'texts must be a non-empty list'}), 400
        
        results = []
        for text in texts:
            if detector and detector.classifier:
                result = detector.predict(text)
            else:
                features = feature_extractor.extract_all_features(text)
                result = {
                    'prediction': None,
                    'ai_probability': None,
                    'extracted_features': features,
                }
            results.append(result)
        
        return jsonify({
            'total': len(results),
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """404 錯誤處理"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 錯誤處理"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("AI Detection System - Flask API Server")
    print("=" * 60)
    print("\nInitializing models...")
    initialize()
    print("✓ Models loaded successfully")
    
    print("\nStarting Flask server...")
    print("Server running at http://localhost:5000")
    print("API Documentation at http://localhost:5000/api")
    print("\nPress CTRL+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
