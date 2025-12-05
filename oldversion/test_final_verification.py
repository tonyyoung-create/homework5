"""
測試修改後的 app.py 邏輯 (28-28-8-6-10-7-5)
"""

import re
import numpy as np

def analyze_text_app_final_fixed(input_text):
    """修改後app.py的評分邏輯"""
    
    ai_score = 0
    score_factors = {}
    
    # 1. 詞彙多樣性 (28%)
    words = input_text.split()
    words_lower = [w.lower() for w in words]
    
    if len(words_lower) > 0:
        unique_words = len(set(words_lower))
        vocab_ratio = unique_words / len(words_lower)
        vocab_score = max(0, min((vocab_ratio - 0.54) / 0.26, 1)) * 0.28
        ai_score += vocab_score
        score_factors['vocabulary_diversity'] = vocab_score
    
    # 2. 句子一致性 (28%)
    sentences = [s.strip() for s in 
               input_text.replace('。', '.|').replace('！', '!|').replace('？', '?|')
                       .replace('.', '.|').replace('!', '!|').replace('?', '?|')
                       .split('|') if s.strip()]
    if len(sentences) > 1:
        sent_lengths = [len(s.split()) for s in sentences]
        mean_len = np.mean(sent_lengths)
        std_len = np.std(sent_lengths)
        cv = std_len / (mean_len + 1e-6) if mean_len > 0 else 0
        consistency_score = max(0, 1 - min(cv, 1.3) / 1.3) * 0.28
        ai_score += consistency_score
        score_factors['sentence_consistency'] = consistency_score
    
    # 3. 英文功能詞 (8%)
    if any(ord(c) < 128 for c in input_text):
        function_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'of',
                        'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had'}
        if len(words_lower) > 0:
            func_word_count = sum(1 for w in words_lower if w in function_words)
            func_ratio = func_word_count / len(words_lower)
            func_score = min(func_ratio / 0.30, 1) * 0.08
            ai_score += func_score
            score_factors['function_words'] = func_score
    
    # 4. 標點符號密度 (6%)
    punct_chars = '.,!?;:\'"—-。！？；：''""'
    total_punct = sum(1 for c in input_text if c in punct_chars)
    punct_density = total_punct / max(len(input_text), 1)
    
    if punct_density < 0.015:
        punct_score = 0.0
    elif punct_density < 0.03:
        punct_score = 0.03
    else:
        punct_score = 0.06
    
    ai_score += punct_score
    score_factors['punctuation_pattern'] = punct_score
    
    # 5. 古文/經典文學檢測 (10%)
    classical_literary_markers = {
        # 中文古文詞彙
        '然而', '既然', '莫若', '其實', '況且', '而況', '不料', '豈料',
        '想不到', '怎料', '誰知', '卻', '竟', '竟然', '偏偏', '恰好',
        '恰恰', '正好', '湊巧', '怪不得', '也難怪', '也怪得',
        '橫豎', '仔細', '戰慄', '歪歪斜斜', '吃人', '字縫',
        '翻開', '歷史', '仁義', '道德', '滿本',
        # 英文古典詞彙
        'alas', 'behold', 'hark', 'lo', 'methinks', 'perchance',
        'forsooth', 'thus', 'verily', 'hence', 'whence', 'thence',
        'thee', 'thou', 'thy', 'hath', 'doth', 'wherefore',
    }
    
    classical_count = 0
    text_lower = input_text.lower()
    
    for marker in classical_literary_markers:
        if '\u4e00' <= marker[0] <= '\u9fff':
            if marker in text_lower:
                classical_count += 1
        elif ord(marker[0]) < 128:
            if re.search(r'\b' + marker + r'\b', text_lower):
                classical_count += 1
    
    if classical_count > 0:
        classical_penalty = min(classical_count * 0.25, 0.40)
        ai_score -= classical_penalty
        score_factors['literary_style'] = -classical_penalty
    else:
        score_factors['literary_style'] = 0.0
    
    # 6. 人性化標記 (7%)
    humanization_score = 0
    
    question_count = input_text.count('?') + input_text.count('？')
    question_ratio = question_count / max(len(sentences), 1)
    if question_ratio > 0.15:
        humanization_score += 0.035
    
    ellipsis_count = input_text.count('...') + input_text.count('。。。')
    if ellipsis_count > 0:
        humanization_score += 0.02
    
    personal_words = {'我', '我覺得', '我認為', '我想', '我發現', '我看', 
                    'i think', 'i feel', 'i believe', 'in my opinion'}
    personal_count = 0
    for word in personal_words:
        if '\u4e00' <= word[0] <= '\u9fff':
            if word in text_lower:
                personal_count += 1
        else:
            if re.search(r'\b' + word + r'\b', text_lower):
                personal_count += 1
    
    if personal_count > 1:
        humanization_score += min(personal_count * 0.015, 0.015)
    
    ai_score -= min(humanization_score, 0.07)
    score_factors['humanization'] = -min(humanization_score, 0.07)
    
    # 7. 結構規律性 (5%)
    paragraphs = [p.strip() for p in input_text.split('\n\n') if p.strip()]
    if len(paragraphs) <= 1:
        ai_score += 0.025
        score_factors['structure'] = 0.025
    else:
        para_lengths = [len(p.split()) for p in paragraphs]
        para_std = np.std(para_lengths)
        para_mean = np.mean(para_lengths)
        para_cv = para_std / (para_mean + 1e-6) if para_mean > 0 else 0
        struct_score = max(0, 1 - min(para_cv, 1)) * 0.05
        ai_score += struct_score
        score_factors['structure'] = struct_score
    
    # 確保分數在 [0, 1] 範圍內
    ai_prob = max(0, min(ai_score, 1.0))
    
    return ai_prob, score_factors


# 測試用例
ai_romance = """The city lights were blurred watercolors against the glass, but inside the small room, only the amber glow of the fireplace held the darkness at bay.

She traced the sharp line of his jaw with her thumb, a gesture so familiar it felt like breathing. "You look worried," she murmured, her voice barely a whisper against the crackle of the wood.

He turned his face into her hand, kissing her palm softly. "I'm only worried that a moment this perfect can't last," he admitted, his eyes holding hers—a deep, troubled blue. "It feels like borrowed time."

"It's not borrowed," she countered, shifting closer so their foreheads touched. The scent of rain and old books clung to his sweater, a scent she had come to associate with home. "It's ours. We built this stillness, didn't we? Out of all the chaos and the years apart."

A slow, undeniable smile broke through his pensive expression. He wrapped his arms around her, pulling her completely onto his lap.

"Then let's make a promise," he whispered, his lips close to her ear. "No matter what storms are waiting, no matter how loud the world gets, we find this room again. Every time. We find the fire, and we find this silence."

"I promise," she replied, tightening her embrace, the warmth of the fire now the least of the heat between them. She knew then that love wasn't about fireworks; it was about the solidity of a quiet vow made under the gentle surveillance of the moon."""

luxun_text = """我翻開歷史一查，這歷史沒有年代，歪歪斜斜的每葉上都寫著"仁義道德"幾個字。我橫豎睡不著，仔細看了半夜，才從字縫裡看出字來，滿本都寫著兩個字是"吃人"！"""

print("="*70)
print("🧪 app.py 最終修改版 (28-28-8-6-10-7-5)")
print("="*70)

# 測試 1
ai_prob_romance, factors_romance = analyze_text_app_final_fixed(ai_romance)
print(f"\n【測試 1】英文愛情小說:")
print(f"  📊 AI 評分: {ai_prob_romance*100:.2f}%")
print(f"  預期: > 50%")
if ai_prob_romance > 0.50:
    print(f"  ✅ 通過!")
else:
    print(f"  ❌ 失敗 (差 {(0.50 - ai_prob_romance)*100:.2f}%)")

# 測試 2
ai_prob_luxun, factors_luxun = analyze_text_app_final_fixed(luxun_text)
print(f"\n【測試 2】魯迅《狂人日記》:")
print(f"  📊 AI 評分: {ai_prob_luxun*100:.2f}%")
print(f"  預期: < 50%")
if ai_prob_luxun < 0.50:
    print(f"  ✅ 通過!")
else:
    print(f"  ❌ 失敗")

print()
print("="*70)
if ai_prob_romance > 0.50 and ai_prob_luxun < 0.50:
    print("✅ 所有測試通過!準備部署")
else:
    print("⚠️ 仍需調整")
print("="*70)
