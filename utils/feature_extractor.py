"""
特徵抽取模組 - 計算 Perplexity、Burstiness、Stylometry 等統計指標
"""

import numpy as np
import re
from typing import Dict, List, Tuple
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords

# 下載必要的 NLTK 資源
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class FeatureExtractor:
    """提取 AI 偵測所需的各項特徵"""
    
    def __init__(self, model_name: str = "distilgpt2"):
        """
        初始化特徵提取器
        
        Args:
            model_name: 使用的語言模型名稱 (預設 distilgpt2 以減少計算量)
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_name = model_name
        
        print(f"Loading model {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()
        
        self.english_stopwords = set(stopwords.words('english'))
        
    def compute_perplexity(self, text: str) -> Dict:
        """
        計算困惑度 (Perplexity) 及相關指標
        
        Args:
            text: 輸入文本
            
        Returns:
            包含 PP、log probability variance 等指標的字典
        """
        inputs = self.tokenizer.encode(text, return_tensors='pt').to(self.device)
        
        with torch.no_grad():
            outputs = self.model(inputs, labels=inputs)
            loss = outputs.loss
            
        # 計算平均 PP
        perplexity = torch.exp(loss).item()
        
        # 獲取每個 token 的 log probability
        with torch.no_grad():
            logits = self.model(inputs).logits
            
        # 計算 log probs 序列
        log_probs = []
        for i in range(len(inputs[0]) - 1):
            logits_i = logits[0, i, :]
            log_prob_i = torch.log_softmax(logits_i, dim=-1)
            token_id = inputs[0, i + 1]
            log_prob = log_prob_i[token_id].item()
            log_probs.append(log_prob)
        
        log_probs = np.array(log_probs)
        
        features = {
            'avg_perplexity': float(perplexity),
            'log_prob_mean': float(np.mean(log_probs)),
            'log_prob_std': float(np.std(log_probs)),
            'log_prob_max': float(np.max(log_probs)),
            'log_prob_min': float(np.min(log_probs)),
            'num_tokens': len(inputs[0]),
        }
        
        return features
    
    def compute_burstiness(self, text: str) -> Dict:
        """
        計算句子節奏指標 (Burstiness)
        
        Args:
            text: 輸入文本
            
        Returns:
            包含 Burstiness、句長統計等指標的字典
        """
        sentences = sent_tokenize(text)
        
        if len(sentences) < 2:
            return {
                'burstiness': 0.0,
                'avg_sentence_length': 0.0,
                'sentence_length_std': 0.0,
                'num_sentences': len(sentences)
            }
        
        # 計算每個句子的單詞數
        sentence_lengths = [len(word_tokenize(s)) for s in sentences]
        
        # Burstiness = std / mean
        mean_len = np.mean(sentence_lengths)
        std_len = np.std(sentence_lengths)
        
        burstiness = std_len / mean_len if mean_len > 0 else 0.0
        
        features = {
            'burstiness': float(burstiness),
            'avg_sentence_length': float(mean_len),
            'sentence_length_std': float(std_len),
            'sentence_length_min': float(np.min(sentence_lengths)),
            'sentence_length_max': float(np.max(sentence_lengths)),
            'num_sentences': len(sentences),
        }
        
        return features
    
    def compute_stylometry(self, text: str) -> Dict:
        """
        計算寫作風格指標 (Stylometry)
        
        Args:
            text: 輸入文本
            
        Returns:
            包含用字、句法、情緒等風格特徵的字典
        """
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        
        # === Lexical Features ===
        # 詞彙多樣性 (Type-Token Ratio)
        unique_words = len(set(w.lower() for w in words if w.isalpha()))
        total_words = len([w for w in words if w.isalpha()])
        ttr = unique_words / total_words if total_words > 0 else 0.0
        
        # 功能詞比例
        function_words = ['the', 'a', 'an', 'is', 'are', 'was', 'were', 
                         'be', 'been', 'being', 'and', 'or', 'but', 'if',
                         'because', 'therefore', 'however', 'thus', 'also']
        func_word_count = sum(1 for w in words if w.lower() in function_words)
        func_word_ratio = func_word_count / len(words) if len(words) > 0 else 0.0
        
        # 稀有詞 (出現 1 次的詞)
        word_freq = Counter(w.lower() for w in words if w.isalpha())
        rare_words = sum(1 for count in word_freq.values() if count == 1)
        rare_word_ratio = rare_words / len(word_freq) if len(word_freq) > 0 else 0.0
        
        # === Syntactic Features ===
        # POS tag 分布
        pos_tags = pos_tag(words)
        pos_counts = Counter(tag for word, tag in pos_tags)
        
        # 代詞 (Pronoun) 比例
        pronouns = [tag for tag, count in pos_counts.items() if tag in ['PRP', 'PRP$', 'WP', 'WP$']]
        pronoun_count = sum(pos_counts.get(p, 0) for p in pronouns)
        pronoun_ratio = pronoun_count / len(words) if len(words) > 0 else 0.0
        
        # 名詞 (Noun) 比例
        noun_count = sum(pos_counts.get(tag, 0) for tag in ['NN', 'NNS', 'NNP', 'NNPS'])
        noun_ratio = noun_count / len(words) if len(words) > 0 else 0.0
        
        # === Emotion & Noise Features ===
        # 感嘆號比例
        exclamation_count = text.count('!')
        exclamation_ratio = exclamation_count / len(sentences) if len(sentences) > 0 else 0.0
        
        # 省略符比例
        ellipsis_count = text.count('...') + text.count('…')
        ellipsis_ratio = ellipsis_count / len(sentences) if len(sentences) > 0 else 0.0
        
        # 大寫字母比例 (情緒指示)
        uppercase_chars = sum(1 for c in text if c.isupper())
        uppercase_ratio = uppercase_chars / len(text) if len(text) > 0 else 0.0
        
        features = {
            # Lexical
            'ttr': float(ttr),
            'func_word_ratio': float(func_word_ratio),
            'rare_word_ratio': float(rare_word_ratio),
            'avg_word_length': float(np.mean([len(w) for w in words if w.isalpha()]) if total_words > 0 else 0),
            
            # Syntactic
            'pronoun_ratio': float(pronoun_ratio),
            'noun_ratio': float(noun_ratio),
            'num_pos_tags': len(pos_counts),
            
            # Emotion & Noise
            'exclamation_ratio': float(exclamation_ratio),
            'ellipsis_ratio': float(ellipsis_ratio),
            'uppercase_ratio': float(uppercase_ratio),
        }
        
        return features
    
    def compute_zipf_features(self, text: str) -> Dict:
        """
        計算 Zipf 長尾分布特徵
        
        Args:
            text: 輸入文本
            
        Returns:
            包含 Zipf 尾部比例等特徵的字典
        """
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalpha()]
        
        if len(words) < 10:
            return {
                'zipf_tail_ratio': 0.0,
                'vocab_size': len(set(words))
            }
        
        word_freq = Counter(words)
        total_unique = len(word_freq)
        
        # 計算前 80% 的詞彙涵蓋的字數比例
        sorted_freqs = sorted(word_freq.values(), reverse=True)
        cumsum = 0
        count_80 = 0
        for freq in sorted_freqs:
            cumsum += freq
            count_80 += 1
            if cumsum >= 0.8 * len(words):
                break
        
        # Zipf tail ratio = 後 20% 的詞彙佔總詞彙的比例
        zipf_tail_ratio = (total_unique - count_80) / total_unique if total_unique > 0 else 0.0
        
        features = {
            'zipf_tail_ratio': float(zipf_tail_ratio),
            'vocab_size': total_unique,
            'vocabulary_richness': float(total_unique / len(words)) if len(words) > 0 else 0,
        }
        
        return features
    
    def extract_all_features(self, text: str) -> Dict:
        """
        提取所有特徵
        
        Args:
            text: 輸入文本
            
        Returns:
            包含所有特徵的字典
        """
        print("Extracting features...")
        
        features = {}
        
        # Perplexity
        try:
            pp_features = self.compute_perplexity(text)
            features.update({f'pp_{k}': v for k, v in pp_features.items()})
        except Exception as e:
            print(f"Warning: Could not compute perplexity: {e}")
            
        # Burstiness
        try:
            burst_features = self.compute_burstiness(text)
            features.update({f'burst_{k}': v for k, v in burst_features.items()})
        except Exception as e:
            print(f"Warning: Could not compute burstiness: {e}")
            
        # Stylometry
        try:
            style_features = self.compute_stylometry(text)
            features.update({f'style_{k}': v for k, v in style_features.items()})
        except Exception as e:
            print(f"Warning: Could not compute stylometry: {e}")
            
        # Zipf
        try:
            zipf_features = self.compute_zipf_features(text)
            features.update({f'zipf_{k}': v for k, v in zipf_features.items()})
        except Exception as e:
            print(f"Warning: Could not compute zipf features: {e}")
        
        return features


if __name__ == "__main__":
    # 測試
    extractor = FeatureExtractor()
    
    test_text = """
    Artificial intelligence is transforming the way we work and live. 
    AI systems can now perform tasks that were once thought to require human intelligence. 
    From natural language processing to computer vision, the applications are endless.
    """
    
    features = extractor.extract_all_features(test_text)
    
    print("\nExtracted Features:")
    for key, value in sorted(features.items()):
        print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")
