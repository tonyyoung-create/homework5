"""
AI 偵測分類器模型
"""

import numpy as np
import pickle
import joblib
from typing import Dict, Tuple
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

from utils.feature_extractor import FeatureExtractor
from utils.data_manager import load_dataset


class AIDetector:
    """AI 文本偵測器"""
    
    def __init__(self, model_path: str = None):
        """
        初始化偵測器
        
        Args:
            model_path: 預訓練模型路徑
        """
        self.feature_extractor = FeatureExtractor()
        self.classifier = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.model_path = model_path
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
    
    def extract_features_batch(self, texts: list) -> np.ndarray:
        """
        批量提取特徵
        
        Args:
            texts: 文本列表
            
        Returns:
            特徵矩陣 (n_samples, n_features)
        """
        feature_list = []
        
        for i, text in enumerate(texts):
            print(f"Processing text {i+1}/{len(texts)}...")
            features = self.feature_extractor.extract_all_features(text)
            feature_list.append(features)
        
        # 轉換為 numpy 矩陣
        if not feature_list:
            return np.array([])
        
        # 確保所有特徵鍵都存在
        all_keys = set()
        for feat_dict in feature_list:
            all_keys.update(feat_dict.keys())
        
        all_keys = sorted(list(all_keys))
        self.feature_names = all_keys
        
        # 構建矩陣
        X = np.zeros((len(feature_list), len(all_keys)))
        for i, feat_dict in enumerate(feature_list):
            for j, key in enumerate(all_keys):
                X[i, j] = feat_dict.get(key, 0.0)
        
        return X
    
    def train(self, dataset_path: str, test_size: float = 0.2, random_state: int = 42):
        """
        訓練偵測器
        
        Args:
            dataset_path: 訓練數據集路徑 (CSV 或 JSON)
            test_size: 測試集比例
            random_state: 隨機種子
            
        Returns:
            訓練結果字典
        """
        print("Loading dataset...")
        data = load_dataset(dataset_path)
        
        texts = [d['text'] for d in data]
        labels = np.array([d['label'] for d in data])
        
        print(f"Extracting features from {len(texts)} texts...")
        X = self.extract_features_batch(texts)
        
        # 分割訓練集和測試集
        X_train, X_test, y_train, y_test = train_test_split(
            X, labels, test_size=test_size, random_state=random_state, stratify=labels
        )
        
        # 標準化特徵
        print("Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # 訓練分類器
        print("Training classifier...")
        self.classifier = LogisticRegression(max_iter=1000, random_state=random_state)
        self.classifier.fit(X_train_scaled, y_train)
        
        # 評估
        y_pred_train = self.classifier.predict(X_train_scaled)
        y_pred_test = self.classifier.predict(X_test_scaled)
        y_prob_test = self.classifier.predict_proba(X_test_scaled)[:, 1]
        
        results = {
            'train_accuracy': accuracy_score(y_train, y_pred_train),
            'test_accuracy': accuracy_score(y_test, y_pred_test),
            'test_precision': precision_score(y_test, y_pred_test),
            'test_recall': recall_score(y_test, y_pred_test),
            'test_f1': f1_score(y_test, y_pred_test),
            'test_roc_auc': roc_auc_score(y_test, y_prob_test),
            'confusion_matrix': confusion_matrix(y_test, y_pred_test).tolist(),
        }
        
        print("\n=== Training Results ===")
        for key, value in results.items():
            if key != 'confusion_matrix':
                print(f"{key}: {value:.4f}")
            else:
                print(f"confusion_matrix: {value}")
        
        return results
    
    def predict(self, text: str) -> Dict:
        """
        預測單個文本
        
        Args:
            text: 輸入文本
            
        Returns:
            預測結果字典，包含概率和特徵
        """
        if self.classifier is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # 提取特徵
        features_dict = self.feature_extractor.extract_all_features(text)
        
        # 轉換為矩陣
        feature_vector = np.zeros(len(self.feature_names))
        for i, name in enumerate(self.feature_names):
            feature_vector[i] = features_dict.get(name, 0.0)
        
        # 標準化
        feature_vector_scaled = self.scaler.transform([feature_vector])
        
        # 預測
        prediction = self.classifier.predict(feature_vector_scaled)[0]
        probability = self.classifier.predict_proba(feature_vector_scaled)[0]
        
        # 獲取特徵重要性（基於模型係數）
        coefficients = self.classifier.coef_[0]
        feature_importance = dict(zip(self.feature_names, coefficients))
        
        # 排序：最重要的特徵優先
        top_features = sorted(
            feature_importance.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:10]
        
        return {
            'prediction': int(prediction),
            'ai_probability': float(probability[1]),
            'human_probability': float(probability[0]),
            'confidence': float(max(probability)),
            'extracted_features': features_dict,
            'top_features': top_features,  # (特徵名, 係數)
        }
    
    def save_model(self, model_path: str):
        """
        保存模型
        
        Args:
            model_path: 模型保存路徑
        """
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'classifier': self.classifier,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
        }
        
        joblib.dump(model_data, model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path: str):
        """
        載入模型
        
        Args:
            model_path: 模型路徑
        """
        model_data = joblib.load(model_path)
        
        self.classifier = model_data['classifier']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        
        print(f"Model loaded from {model_path}")


if __name__ == "__main__":
    # 訓練模型
    detector = AIDetector()
    
    # 確保數據集存在
    dataset_path = 'data/training_data_en.csv'
    
    # 如果數據集不存在，先生成
    if not Path(dataset_path).exists():
        from utils.data_manager import create_dataset
        create_dataset(dataset_path, language='english')
    
    # 訓練
    results = detector.train(dataset_path)
    
    # 保存模型
    detector.save_model('models/ai_detector_model.pkl')
    
    # 測試預測
    test_text = "This is a test text generated by an AI system."
    prediction = detector.predict(test_text)
    
    print("\n=== Test Prediction ===")
    print(f"Text: {test_text}")
    print(f"AI Probability: {prediction['ai_probability']:.4f}")
    print(f"Human Probability: {prediction['human_probability']:.4f}")
    print(f"Confidence: {prediction['confidence']:.4f}")
    print("\nTop 5 Important Features:")
    for feat_name, coeff in prediction['top_features'][:5]:
        print(f"  {feat_name}: {coeff:.4f}")
