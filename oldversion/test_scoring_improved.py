#!/usr/bin/env python3
"""
改進的評分測試 - 包含文學風格檢測
支援經典文學作品識別
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

# 測試文本

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

# 魯迅《狂人日記》片段
luxun_text = """
我翻開歷史一查，這歷史沒有年代，歪歪斜斜的每葉上都寫著"仁義道德"幾個字。
我橫豎睡不著，仔細看了半夜，才從字縫裡看出字來，滿本都寫著兩個字是"吃人"！
我這回可是真的被嚇壞了；趕緊合上歷史；心裡卻突然一陣很冷的戰慄。
"""

def score_text(text):
    """使用改進的評分邏輯 - 包含文學風格檢測"""
    ai_score = 0
    score_factors = {}
    
    # 清理文本
    words = text.split()
    words_lower = [w.lower() for w in words]
    
    # 1. 詞彙多樣性 (35%)
    if len(words_lower) > 0:
        unique_words = len(set(words_lower))
        vocab_ratio = unique_words / len(words_lower)
        vocab_score = max(0, min((vocab_ratio - 0.5) / 0.3, 1)) * 0.35
        ai_score += vocab_score
        score_factors['vocabulary_diversity'] = vocab_score
    
    # 2. 句子一致性 (35%)
    sentences = [s.strip() for s in 
               text.replace('。', '.|').replace('！', '!|').replace('？', '?|')
                   .replace('.', '.|').replace('!', '!|').replace('?', '?|')
                   .split('|') if s.strip()]
    if len(sentences) > 1:
        sent_lengths = [len(s.split()) for s in sentences]
        mean_len = np.mean(sent_lengths)
        std_len = np.std(sent_lengths)
        cv = std_len / (mean_len + 1e-6) if mean_len > 0 else 0
        consistency_score = max(0, 1 - min(cv, 1.2) / 1.2) * 0.35
        ai_score += consistency_score
        score_factors['sentence_consistency'] = consistency_score
    
    # 3. 功能詞 (10%)
    if any(ord(c) < 128 for c in text):
        function_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'of',
                         'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had'}
        if len(words_lower) > 0:
            func_word_count = sum(1 for w in words_lower if w in function_words)
            func_ratio = func_word_count / len(words_lower)
            func_score = min(func_ratio / 0.30, 1) * 0.10
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
    
    # 5. 文學風格檢測 (15%) - 新增
    # AI 通常避免使用文學性措辭、比喻、擬人法等
    literary_markers = {
        # 中文文學詞彙
        '然而', '既然', '莫若', '其實', '況且', '而況', '不料', '豈料',
        '想不到', '怎料', '誰知', '卻', '竟', '竟然', '偏偏', '恰好',
        '恰恰', '正好', '湊巧', '怪不得', '也難怪', '也怪得',
        '悲哀', '淒涼', '蒼涼', '荒涼', '寂寥', '孤寂', '頹廢',
        '迷茫', '困頓', '抑鬱', '沉悶', '壓抑', '窒息',
        '呢喃', '低聲', '輕聲', '細語', '喃喃', '囈語',
        '汨汨', '潺潺', '淙淙', '悠悠', '悄悄', '默默',
        '飄飄然', '渺渺然', '茫茫然', '憑添', '添增', '衍生',
        '橫豎', '仔細', '戰慄', '歪歪斜斜', '字縫', '吃人',
        # 英文文學詞彙
        'alas', 'behold', 'hark', 'lo', 'methinks', 'perchance',
        'forsooth', 'thus', 'verily', 'hence', 'whence', 'thence',
        'woe', 'sorrow', 'anguish', 'melancholy', 'languish',
    }
    
    literary_count = 0
    for marker in literary_markers:
        if marker in text.lower():
            literary_count += 1
    
    # 文學詞彙越多，越不像 AI (所以減低分數)
    literary_density = literary_count / max(len(words_lower) / 100, 1)
    # 高文學密度 -> 低 AI 分數
    literary_score = max(0, 1 - min(literary_density * 0.5, 1)) * 0.15
    ai_score -= literary_score * 0.5  # 減低 AI 分數
    score_factors['literary_style'] = -literary_score * 0.5
    
    # 6. 結構 (5%)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) <= 1:
        ai_score += 0.02
        score_factors['structure'] = 0.02
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


# 顏色定義
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
END = '\033[0m'

print(f"\n{BLUE}{'='*70}")
print("  AI 偵測系統 - 改進版評分測試 (含文學風格檢測)")
print(f"{'='*70}{END}\n")

test_cases = [
    ("🤖 AI 生成文本", ai_text, True),
    ("👤 人類文本", human_text, False),
    ("📚 魯迅《狂人日記》", luxun_text, False),
]

print("測試結果:\n")

results = []
for name, text, is_ai in test_cases:
    ai_prob, factors = score_text(text)
    results.append((name, ai_prob, is_ai))
    
    # 判定
    if is_ai and ai_prob > 0.5:
        status = f"{GREEN}✅ 正確{END}"
    elif not is_ai and ai_prob < 0.5:
        status = f"{GREEN}✅ 正確{END}"
    else:
        status = f"{YELLOW}⚠️  誤判{END}"
    
    print(f"{name:20} → {ai_prob:6.2%} AI {status}")
    print(f"   分數因子:")
    for k, v in factors.items():
        if v != 0:
            print(f"     - {k:25} = {v:+.3f}")
    print()

# 驗證結果
print(f"{BLUE}{'='*70}{END}")
print("驗證結果:\n")

success = 0
total = len(test_cases)

for name, ai_prob, is_ai in results:
    if is_ai and ai_prob > 0.5:
        print(f"{GREEN}✅{END} {name:20} → {ai_prob:.2%} AI (正確)")
        success += 1
    elif not is_ai and ai_prob < 0.5:
        print(f"{GREEN}✅{END} {name:20} → {ai_prob:.2%} AI (正確)")
        success += 1
    else:
        print(f"{RED}❌{END} {name:20} → {ai_prob:.2%} AI (誤判)")

print(f"\n測試通過率: {success}/{total} ({100*success//total}%)")

if success == total:
    print(f"\n{GREEN}✅ 所有測試通過！文學風格檢測工作正常！{END}\n")
else:
    print(f"\n{YELLOW}⚠️  部分測試未通過，請檢查評分邏輯{END}\n")
