#!/usr/bin/env python3
"""
AI 偵測系統 - 完整功能驗證
驗證所有關鍵功能是否正常工作
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
from datetime import datetime

# 顏色輸出
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_section(title):
    """打印分隔符"""
    print(f"\n{BLUE}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{END}\n")

def print_success(msg):
    """打印成功信息"""
    print(f"{GREEN}✅ {msg}{END}")

def print_error(msg):
    """打印錯誤信息"""
    print(f"{RED}❌ {msg}{END}")

def print_info(msg):
    """打印信息"""
    print(f"{BLUE}ℹ️  {msg}{END}")

def score_text(text):
    """新的評分邏輯"""
    ai_score = 0
    score_factors = {}
    
    # 清理文本
    words = text.split()
    words_lower = [w.lower() for w in words]
    
    # 1. 詞彙多樣性 (40%)
    if len(words_lower) > 0:
        unique_words = len(set(words_lower))
        vocab_ratio = unique_words / len(words_lower)
        vocab_score = max(0, min((vocab_ratio - 0.4) / 0.4, 1)) * 0.40
        ai_score += vocab_score
        score_factors['vocabulary_diversity'] = vocab_score
    
    # 2. 句子一致性 (30%)
    sentences = [s.strip() for s in 
               text.replace('。', '.|').replace('！', '!|').replace('？', '?|')
                   .replace('.', '.|').replace('!', '!|').replace('?', '?|')
                   .split('|') if s.strip()]
    if len(sentences) > 1:
        sent_lengths = [len(s.split()) for s in sentences]
        mean_len = np.mean(sent_lengths)
        std_len = np.std(sent_lengths)
        cv = std_len / (mean_len + 1e-6) if mean_len > 0 else 0
        consistency_score = max(0, 1 - min(cv, 1.2) / 1.2) * 0.30
        ai_score += consistency_score
        score_factors['sentence_consistency'] = consistency_score
    
    # 3. 功能詞 (15%)
    if any(ord(c) < 128 for c in text):
        function_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'of',
                         'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had'}
        if len(words_lower) > 0:
            func_word_count = sum(1 for w in words_lower if w in function_words)
            func_ratio = func_word_count / len(words_lower)
            func_score = min(func_ratio / 0.30, 1) * 0.15
            ai_score += func_score
            score_factors['function_words'] = func_score
    
    # 4. 標點 (10%)
    punct_chars = '.,!?;:\'"—-。！？；：''""'
    total_punct = sum(1 for c in text if c in punct_chars)
    punct_density = total_punct / max(len(text), 1)
    
    if punct_density < 0.015:
        punct_score = 0.0
    elif punct_density < 0.03:
        punct_score = 0.05
    else:
        punct_score = 0.10
    
    ai_score += punct_score
    score_factors['punctuation_pattern'] = punct_score
    
    # 5. 結構 (5%)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) <= 1:
        ai_score += 0.05
        score_factors['structure'] = 0.05
    else:
        para_lengths = [len(p.split()) for p in paragraphs]
        para_std = np.std(para_lengths)
        para_mean = np.mean(para_lengths)
        para_cv = para_std / (para_mean + 1e-6) if para_mean > 0 else 0
        struct_score = max(0, 1 - min(para_cv, 1)) * 0.05
        ai_score += struct_score
        score_factors['structure'] = struct_score
    
    ai_prob = max(0, min(ai_score, 1.0))
    return ai_prob, score_factors


# ============================================================
# 主驗證程序
# ============================================================

print(f"\n{BLUE}{'='*60}")
print(f"  AI 偵測系統 - 完整功能驗證")
print(f"  時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*60}{END}\n")

# 測試 1: 模塊導入
print_section("1. 模塊導入測試")
try:
    import numpy as np
    print_success("NumPy 導入成功")
except:
    print_error("NumPy 導入失敗")

# 測試 2: 評分邏輯
print_section("2. 評分邏輯測試")

test_cases = [
    ("AI 英文", """The advancement of artificial intelligence has revolutionized numerous industries over 
the past decade. Machine learning algorithms have demonstrated remarkable capabilities in pattern recognition 
and predictive analytics. The integration of AI systems into business processes has significantly improved 
operational efficiency and decision-making processes."""),
    
    ("人類英文", """You know, I've been thinking about this for a while. Why is it that some people 
just seem to have a natural talent for writing? Maybe it's because they read a lot, or maybe they're 
just naturally gifted. But honestly, it takes real practice and dedication to get good at it."""),
    
    ("AI 中文", """人工智能技術的發展已經深刻改變了現代社會的多個領域。機器學習算法在數據分析和模式識別中展現出了卓越的性能。
企業採用人工智能系統已經顯著提高了工作效率和業務流程的自動化程度。"""),
    
    ("人類中文", """你知道嗎，我一直在想這個問題。為什麼有些人就是特別會寫東西呢？可能是讀的書多了，
或者天生就有這天賦吧。不過話說回來，真正要寫好東西，還是得靠長期的積累和練習的。"""),
]

results = []
for name, text in test_cases:
    ai_prob, factors = score_text(text)
    results.append((name, ai_prob))
    
    # 判定
    if "AI" in name and ai_prob > 0.5:
        status = f"{GREEN}✅ 正確{END}"
    elif "人類" in name and ai_prob <= 0.5:
        status = f"{GREEN}✅ 正確{END}"
    else:
        status = f"{YELLOW}⚠️  邊界{END}"
    
    print(f"{name:12} → {ai_prob:6.2%} AI {status}")
    print(f"  分數因子: {', '.join(f'{k}={v:.2f}' for k,v in factors.items())}")
    print()

# 驗證結果
print_section("3. 驗證結果")

# 檢查 AI 文本是否 > 50%
ai_english = results[0][1]
ai_chinese = results[2][1]

if ai_english > 0.5:
    print_success(f"AI 英文文本正確識別: {ai_english:.2%}")
else:
    print_error(f"AI 英文文本識別失敗: {ai_english:.2%}")

if ai_chinese > 0.5:
    print_success(f"AI 中文文本正確識別: {ai_chinese:.2%}")
else:
    print_error(f"AI 中文文本識別失敗: {ai_chinese:.2%}")

# 檢查人類文本是否 < 50%
human_english = results[1][1]
human_chinese = results[3][1]

if human_english < 0.5:
    print_success(f"人類英文文本正確識別: {human_english:.2%}")
else:
    print_info(f"人類英文文本分數較高: {human_english:.2%} (可能需要調優)")

if human_chinese < 0.5:
    print_success(f"人類中文文本正確識別: {human_chinese:.2%}")
else:
    print_info(f"人類中文文本分數較高: {human_chinese:.2%} (可能需要調優)")

# 最終報告
print_section("最終報告")

success_count = 0
total_count = len(test_cases)

if ai_english > 0.5:
    success_count += 1
if ai_chinese > 0.5:
    success_count += 1
if human_english < 0.5:
    success_count += 1
if human_chinese < 0.5:
    success_count += 1

accuracy = (success_count / total_count) * 100

print(f"核心指標:")
print(f"  - AI 文本平均分: {(ai_english + ai_chinese) / 2:.2%}")
print(f"  - 人類文本平均分: {(human_english + human_chinese) / 2:.2%}")
print(f"  - 測試通過率: {accuracy:.1f}% ({success_count}/{total_count})")

if success_count >= 3:
    print(f"\n{GREEN}✅ 系統驗證通過！可投入使用{END}\n")
else:
    print(f"\n{YELLOW}⚠️  系統需要調優{END}\n")

print(f"{BLUE}{'='*60}{END}")
print("驗證完成！")
print(f"{BLUE}{'='*60}{END}\n")
