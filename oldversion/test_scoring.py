#!/usr/bin/env python3
"""
測試改進的評分邏輯
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

# AI 生成的文本
ai_text = """
The development of artificial intelligence has become increasingly significant in recent years. 
The technological advancements have led to numerous applications across various industries. 
The implementation of machine learning algorithms has resulted in improved efficiency and accuracy. 
The analysis of data has become more sophisticated and comprehensive. 
The future of technology appears to be closely linked with artificial intelligence.
"""

# 人類寫的文本
human_text = """
你知道嗎，我最近在想一個問題。為什麼有些人就是特別擅長寫東西？
可能是因為他們讀得多，或者就是天生的才華吧。不過話說回來，
寫好東西真的不容易。要把想法清楚地表達出來，還要讓人感興趣，
這需要時間和練習。我覺得最重要的是要有真實的想法，
而不是機械地拼湊詞彙。你同意嗎？
"""

def score_text(text):
    """使用強化的評分邏輯 - 最優化版本"""
    ai_score = 0
    score_factors = {}
    
    # 清理和準備文本
    words = text.split()
    words_lower = [w.lower() for w in words]
    text_lower = text.lower()
    
    # 1. 詞重複度 (最重要的指標) - 權重提升到 40%
    if len(words_lower) > 0:
        unique_words = len(set(words_lower))
        vocab_ratio = unique_words / len(words_lower)  # TTR: Type-Token Ratio
        # AI: TTR 高 (0.6-0.8) -> 高分
        # 人類: TTR 低 (0.4-0.6) -> 低分
        # 將 TTR 0.4-0.8 映射到 0-1
        vocab_score = max(0, min((vocab_ratio - 0.4) / 0.4, 1)) * 0.40
        ai_score += vocab_score
        score_factors['vocabulary_diversity'] = vocab_score
    
    # 2. 文本流暢性 - 句子長度變異係數 (30%)
    sentences = [s.strip() for s in 
               text.replace('。', '.|').replace('！', '!|').replace('？', '?|')
                   .replace('.', '.|').replace('!', '!|').replace('?', '?|')
                   .split('|') if s.strip()]
    if len(sentences) > 1:
        sent_lengths = [len(s.split()) for s in sentences]
        mean_len = np.mean(sent_lengths)
        std_len = np.std(sent_lengths)
        cv = std_len / (mean_len + 1e-6) if mean_len > 0 else 0
        # CV < 0.3 = 人類自然, CV > 0.8 = AI 機械
        # 反轉邏輯：高 CV = 人類, 低 CV = AI
        consistency_score = max(0, 1 - min(cv, 1.2) / 1.2) * 0.30
        ai_score += consistency_score
        score_factors['sentence_consistency'] = consistency_score
    
    # 3. 詞類分布 (低權重，因為語言差異) - 15%
    # 只在英文時有效
    if any(ord(c) < 128 for c in text):  # 檢測是否有英文字符
        function_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'of',
                         'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had'}
        if len(words_lower) > 0:
            func_word_count = sum(1 for w in words_lower if w in function_words)
            func_ratio = func_word_count / len(words_lower)
            func_score = min(func_ratio / 0.30, 1) * 0.15
            ai_score += func_score
            score_factors['function_words'] = func_score
    
    # 4. 標點符號模式 (10%)
    punct_chars = '.,!?;:\'"—-。！？；：''""'
    total_punct = sum(1 for c in text if c in punct_chars)
    punct_density = total_punct / max(len(text), 1)
    
    # AI 文本標點密度通常 0.02-0.04，人類 0.01-0.03
    if punct_density < 0.015:
        punct_score = 0.0  # 人類傾向
    elif punct_density < 0.03:
        punct_score = 0.05
    else:
        punct_score = 0.10  # AI 傾向
    
    ai_score += punct_score
    score_factors['punctuation_pattern'] = punct_score
    
    # 5. 沒有段落結構 (5%)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) <= 1:
        # 單段落 = 可能 AI
        ai_score += 0.05
        score_factors['structure'] = 0.05
    else:
        # 有多段落 = 更像人類
        para_lengths = [len(p.split()) for p in paragraphs]
        para_std = np.std(para_lengths)
        para_mean = np.mean(para_lengths)
        para_cv = para_std / (para_mean + 1e-6) if para_mean > 0 else 0
        # 低變異 = AI
        struct_score = max(0, 1 - min(para_cv, 1)) * 0.05
        ai_score += struct_score
        score_factors['structure'] = struct_score
    
    ai_prob = max(0, min(ai_score, 1.0))
    return ai_prob, score_factors

print("=" * 60)
print("AI 偵測系統 - 評分邏輯測試")
print("=" * 60)

print("\n📊 AI 生成的文本評分：")
ai_prob_ai, factors_ai = score_text(ai_text)
print(f"AI 概率: {ai_prob_ai:.2%}")
print(f"分數因子：{factors_ai}")
print(f"判定結果: {'🤖 AI 生成' if ai_prob_ai >= 0.5 else '👤 人類撰寫'}")

print("\n" + "=" * 60)
print("\n📊 人類寫的文本評分：")
ai_prob_human, factors_human = score_text(human_text)
print(f"AI 概率: {ai_prob_human:.2%}")
print(f"分數因子：{factors_human}")
print(f"判定結果: {'🤖 AI 生成' if ai_prob_human >= 0.5 else '👤 人類撰寫'}")

print("\n" + "=" * 60)
print(f"\n✅ 測試完成！")
print(f"預期：AI 文本 > 50%, 人類文本 < 50%")
print(f"實際：AI {ai_prob_ai:.2%}, 人類 {ai_prob_human:.2%}")

if ai_prob_ai > ai_prob_human:
    print("✅ 評分邏輯正常工作！")
else:
    print("⚠️ 評分邏輯需要調整")
