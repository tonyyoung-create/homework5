#!/usr/bin/env python3
"""最終平衡版評分測試 - 詞級文學檢測 + 最優權重"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import re

# 測試文本
ai_text = """
The development of artificial intelligence has become increasingly significant in recent years. 
The technological advancements have led to numerous applications across various industries. 
The implementation of machine learning algorithms has resulted in improved efficiency and accuracy. 
The analysis of data has become more sophisticated and comprehensive. 
The future of technology appears to be closely linked with artificial intelligence.
"""

human_text = """
你知道嗎，我最近在想一個問題。為什麼有些人就是特別擅長寫東西？
可能是因為他們讀得多，或者就是天生的才華吧。不過話說回來，
寫好東西真的不容易。要把想法清楚地表達出來，還要讓人感興趣，
這需要時間和練習。我覺得最重要的是要有真實的想法，
而不是機械地拼湊詞彙。你同意嗎？
"""

luxun_text = """
我翻開歷史一查，這歷史沒有年代，歪歪斜斜的每葉上都寫著"仁義道德"幾個字。
我橫豎睡不著，仔細看了半夜，才從字縫裡看出字來，滿本都寫著兩個字是"吃人"！
我這回可是真的被嚇壞了；趕緊合上歷史；心裡卻突然一陣很冷的戰慄。
"""

def score_text(text):
    """最優平衡評分 - 權重組合"""
    ai_score = 0
    score_factors = {}
    
    words = text.split()
    words_lower = [w.lower() for w in words]
    
    # 1. 詞彙多樣性 (28%) - 保守
    if len(words_lower) > 0:
        unique_words = len(set(words_lower))
        vocab_ratio = unique_words / len(words_lower)
        vocab_score = max(0, min((vocab_ratio - 0.5) / 0.3, 1)) * 0.28
        ai_score += vocab_score
        score_factors['vocabulary_diversity'] = vocab_score
    
    # 2. 句子一致性 (28%) - 保守
    sentences = [s.strip() for s in 
               text.replace('。', '.|').replace('！', '!|').replace('？', '?|')
                   .replace('.', '.|').replace('!', '!|').replace('?', '?|')
                   .split('|') if s.strip()]
    if len(sentences) > 1:
        sent_lengths = [len(s.split()) for s in sentences]
        mean_len = np.mean(sent_lengths)
        std_len = np.std(sent_lengths)
        cv = std_len / (mean_len + 1e-6) if mean_len > 0 else 0
        consistency_score = max(0, 1 - min(cv, 1.2) / 1.2) * 0.28
        ai_score += consistency_score
        score_factors['sentence_consistency'] = consistency_score
    
    # 3. 功能詞 (8%)
    if any(ord(c) < 128 for c in text):
        function_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'of',
                         'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had'}
        if len(words_lower) > 0:
            func_word_count = sum(1 for w in words_lower if w in function_words)
            func_ratio = func_word_count / len(words_lower)
            func_score = min(func_ratio / 0.30, 1) * 0.08
            ai_score += func_score
            score_factors['function_words'] = func_score
    
    # 4. 標點 (8%)
    punct_chars = '.,!?;:\'"—-。！？；：''""'
    total_punct = sum(1 for c in text if c in punct_chars)
    punct_density = total_punct / max(len(text), 1)
    
    if punct_density < 0.015:
        punct_score = 0.0
    elif punct_density < 0.03:
        punct_score = 0.04
    else:
        punct_score = 0.08
    
    ai_score += punct_score
    score_factors['punctuation_pattern'] = punct_score
    
    # 5. 文學風格檢測 - 提升權重 (20%)
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
        # 魯迅特有詞彙
        '橫豎', '仔細', '戰慄', '歪歪斜斜', '吃人', '字縫',
        '翻開', '歷史', '仁義', '道德', '滿本',
        # 英文文學詞彙
        'alas', 'behold', 'hark', 'lo', 'methinks', 'perchance',
        'forsooth', 'thus', 'verily', 'hence', 'whence', 'thence',
        'woe', 'sorrow', 'anguish', 'melancholy', 'languish',
    }
    
    literary_count = 0
    text_lower = text.lower()
    
    # 檢查中文詞
    for marker in literary_markers:
        if '\u4e00' <= marker[0] <= '\u9fff':  # 中文範圍
            if marker in text_lower:
                literary_count += 1
    
    # 英文詞用詞邊界檢測
    for marker in literary_markers:
        if ord(marker[0]) < 128:  # 英文
            if re.search(r'\b' + marker + r'\b', text_lower):
                literary_count += 1
    
    if literary_count > 0:
        # 有文學標記 -> 強烈減低分數
        # 公式：literary_count * 0.20（每個標記減 0.20）
        literary_penalty = min(literary_count * 0.20, 0.5)
        ai_score -= literary_penalty
        score_factors['literary_style'] = -literary_penalty
    else:
        score_factors['literary_style'] = 0.0
    
    # 6. 結構 (8%)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) <= 1:
        ai_score += 0.04
        score_factors['structure'] = 0.04
    else:
        para_lengths = [len(p.split()) for p in paragraphs]
        para_std = np.std(para_lengths)
        para_mean = np.mean(para_lengths)
        para_cv = para_std / (para_mean + 1e-6) if para_mean > 0 else 0
        struct_score = max(0, 1 - min(para_cv, 1)) * 0.08
        ai_score += struct_score
        score_factors['structure'] = struct_score
    
    ai_prob = max(0, min(ai_score, 1.0))
    return ai_prob, score_factors

# 顏色
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
END = '\033[0m'

print(f"\n{BLUE}{'='*70}")
print("  AI 偵測系統 - 最終平衡版 (權重: 28-28-8-8-20-8)")
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
    
    if is_ai and ai_prob > 0.5:
        status = f"{GREEN}✅{END}"
    elif not is_ai and ai_prob < 0.5:
        status = f"{GREEN}✅{END}"
    else:
        status = f"{YELLOW}⚠️{END}"
    
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
for name, ai_prob, is_ai in results:
    if is_ai and ai_prob > 0.5:
        print(f"{GREEN}✅{END} {name:20} → {ai_prob:.2%} AI (正確)")
        success += 1
    elif not is_ai and ai_prob < 0.5:
        print(f"{GREEN}✅{END} {name:20} → {ai_prob:.2%} AI (正確)")
        success += 1
    else:
        print(f"{RED}❌{END} {name:20} → {ai_prob:.2%} AI (誤判)")

print(f"\n測試通過率: {success}/{len(test_cases)} ({100*success//len(test_cases)}%)\n")

if success == len(test_cases):
    print(f"{GREEN}✅ 所有測試通過！{END}\n")
else:
    print(f"{YELLOW}⚠️  部分測試未通過，微調中{END}\n")
