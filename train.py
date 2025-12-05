#!/usr/bin/env python3
"""
訓練腳本 - 用於線下訓練 AI 偵測模型
"""

import sys
from pathlib import Path

# 添加專案路徑
sys.path.insert(0, str(Path(__file__).parent))

from utils.data_manager import create_dataset, create_json_dataset
from models.ai_detector import AIDetector


def main():
    print("=" * 60)
    print("AI Detection System - Model Training Script")
    print("=" * 60)
    
    # Step 1: 建立訓練數據集
    print("\n[Step 1] Creating training datasets...")
    
    try:
        create_dataset('data/training_data_en.csv', language='english')
        create_json_dataset('data/training_data_en.json', language='english')
        print("✓ English dataset created successfully")
    except Exception as e:
        print(f"✗ Error creating English dataset: {e}")
        return
    
    try:
        create_dataset('data/training_data_cn.csv', language='chinese')
        create_json_dataset('data/training_data_cn.json', language='chinese')
        print("✓ Chinese dataset created successfully")
    except Exception as e:
        print(f"✗ Error creating Chinese dataset: {e}")
    
    # Step 2: 訓練模型
    print("\n[Step 2] Training detector model...")
    
    detector = AIDetector()
    
    try:
        results = detector.train(
            dataset_path='data/training_data_en.csv',
            test_size=0.2,
            random_state=42
        )
        
        print("\n" + "=" * 60)
        print("TRAINING RESULTS")
        print("=" * 60)
        print(f"Train Accuracy:  {results['train_accuracy']:.4f}")
        print(f"Test Accuracy:   {results['test_accuracy']:.4f}")
        print(f"Precision:       {results['test_precision']:.4f}")
        print(f"Recall:          {results['test_recall']:.4f}")
        print(f"F1 Score:        {results['test_f1']:.4f}")
        print(f"ROC-AUC:         {results['test_roc_auc']:.4f}")
        print("Confusion Matrix:")
        print(f"  TN: {results['confusion_matrix'][0][0]}")
        print(f"  FP: {results['confusion_matrix'][0][1]}")
        print(f"  FN: {results['confusion_matrix'][1][0]}")
        print(f"  TP: {results['confusion_matrix'][1][1]}")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Error training model: {e}")
        return
    
    # Step 3: 保存模型
    print("\n[Step 3] Saving model...")
    
    try:
        detector.save_model('models/ai_detector_model.pkl')
        print("✓ Model saved to models/ai_detector_model.pkl")
    except Exception as e:
        print(f"✗ Error saving model: {e}")
        return
    
    # Step 4: 測試模型
    print("\n[Step 4] Testing model on sample texts...")
    
    test_samples = [
        ("This is a paragraph about artificial intelligence. "
         "AI has revolutionized many industries. "
         "Machine learning is a subset of artificial intelligence. "
         "Deep learning uses neural networks.", "AI-generated"),
        
        ("omg i cant believe this is happening to me rn!!! "
         "like literally i didnt expect this at all. "
         "anyway so im gonna just go with it i guess lol", "Human"),
    ]
    
    for text, expected in test_samples:
        result = detector.predict(text)
        pred_label = "AI" if result['prediction'] == 1 else "Human"
        print(f"\nText: {text[:60]}...")
        print(f"Expected: {expected}, Predicted: {pred_label}")
        print(f"AI Probability: {result['ai_probability']:.4f}")
        print(f"Confidence: {result['confidence']:.4f}")
    
    print("\n" + "=" * 60)
    print("Training complete! Model is ready for deployment.")
    print("=" * 60)


if __name__ == "__main__":
    main()
