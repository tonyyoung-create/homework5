"""
生成與管理訓練、驗證數據集
"""

import json
import csv
from pathlib import Path
from typing import List, Dict

# 真實 Human 文本樣本
HUMAN_SAMPLES = [
    "你知道嗎？我今天在路上看到一隻超大的烏鴉，真的是超扯。而且牠還搶走我朋友的便當，哈哈哈。然後朋友就很生氣，追著烏鴉跑了一整條街。太扯了。",
    
    "嗯其實我覺得這個方案有點問題啦。首先成本太高，其次實行困難。但如果改一下的話應該還有救。不過要看老闆同不同意就是了。真的是頭痛耶……",
    
    "剛剛有個會議超無聊欸。那個人一直在講廢話，我整個人快睡著了。最後還被老闆點名回答問題，我完全沒在聽 😭 尷尬到爆炸。",
    
    "AI 現在真的很厲害欸！但我還是有點怕它會搶走我們的工作啦。不過話說回來，也滿便利的就是，很多事情都可以交給它做。感覺是雙面刃吧。",
    
    "天啊！我昨天晚上熬夜看劇，早上起不來，遲到了 20 分鐘。結果被主管罵到臭頭。真的超後悔啦，以後再也不熬夜了……（才怪）",
    
    "欸你有沒有看到新聞？說國外那邊又發生什麼事情。我覺得現在的世界真的有點亂欸。不過我也懶得一個一個去了解，就看看有沒有人來跟我講。",
    
    "我最近在學 Python，但是真的超難的啦！一堆概念都搞不懂，每次寫程式都會出現一堆 error。氣死了。不過有時候成功執行的時候還滿有成就感的啦。",
]

# AI 生成文本樣本（模擬 ChatGPT / GPT-3.5 等模型的輸出）
AI_SAMPLES = [
    "Artificial intelligence represents a paradigm shift in how we approach problem-solving. Machine learning algorithms have demonstrated remarkable capabilities across diverse domains, from natural language processing to computer vision. The integration of deep learning techniques has enabled systems to achieve performance levels previously thought impossible. As AI continues to evolve, it is crucial to consider both the opportunities and challenges it presents to society.",
    
    "The implementation of modern cloud infrastructure has revolutionized data management practices. Organizations can now leverage scalable computing resources to process vast amounts of information efficiently. This technological advancement facilitates real-time analytics and enables businesses to make data-driven decisions more effectively. Furthermore, the adoption of cloud-based solutions reduces operational costs while improving system reliability and accessibility.",
    
    "The field of renewable energy is experiencing significant growth as global awareness of climate change increases. Solar and wind power technologies have become increasingly cost-effective and efficient. Government incentives and corporate investments are accelerating the transition toward sustainable energy sources. This shift not only addresses environmental concerns but also creates new economic opportunities in the clean energy sector.",
    
    "Cybersecurity has become an essential component of modern business operations. As digital threats continue to evolve, organizations must implement comprehensive security measures to protect their systems and data. The adoption of multi-factor authentication, encryption protocols, and regular security audits helps mitigate potential vulnerabilities. Training employees on security best practices remains a critical element in maintaining a robust security posture.",
    
    "Digital transformation initiatives have fundamentally altered the landscape of contemporary business. Organizations that successfully implement digital strategies gain competitive advantages through improved efficiency and customer engagement. The integration of artificial intelligence, cloud computing, and big data analytics enables companies to optimize their operations and deliver enhanced value to stakeholders. As technology continues to advance, the pace of digital transformation is expected to accelerate further.",
    
    "The application of machine learning techniques in healthcare has demonstrated considerable promise in improving diagnostic accuracy and treatment outcomes. Predictive models can identify disease patterns and risk factors, enabling healthcare professionals to intervene proactively. The analysis of large medical datasets facilitates the discovery of novel therapeutic approaches and personalized medicine strategies. However, the implementation of these technologies requires careful consideration of ethical implications and data privacy concerns.",
    
    "E-commerce platforms have transformed consumer shopping behavior and retail business models. The convenience of online shopping, combined with personalized recommendations powered by machine learning algorithms, has significantly increased customer engagement. Supply chain optimization through data analytics ensures efficient inventory management and timely product delivery. These technological innovations have created unprecedented opportunities for businesses to expand their market reach and enhance customer satisfaction.",
]

# 中文版本
HUMAN_SAMPLES_CN = [
    "天啦，我今天在課堂上完全沒聽課，老師一直在講什麼我根本不知道。而且還被點名回答問題，我只能說不知道。超尷尬的啦……下次一定要認真聽。（騙人）",
    
    "這個案子真的很複雜欸。首先客戶的需求一直在變，其次我們的技術可能不足以應對。但反正就先試試看吧，死馬當活馬醫。希望不要出太大的問題啦。",
    
    "昨天熬夜打遊戲，今天上班超累。一整天都在打哈欠，同事還問我是不是生病了哈哈。真的要改掉這個壞習慣……但遊戲太好玩了啦！",
    
    "現在的 AI 助手真的很強欸，可以幫我寫文案、寫程式、甚至寫作業。不過總覺得有點怪怪的，感覺有點太簡單了？但又不能拒絕這種便利啦。",
]

AI_SAMPLES_CN = [
    "人工智慧技術正在逐步改變人類社會的各個領域。通過深度學習和機器學習算法的應用，系統可以實現自動化決策和智能分析。自然語言處理的進步使得人機交互變得更加自然流暢。隨著技術的不斷演進，我們可以預期人工智慧將在未來發揮越來越重要的作用。",
    
    "數字化轉型已成為現代企業發展的必然趨勢。組織通過整合雲計算、大數據分析和物聯網技術，能夠顯著提升運營效率和決策質量。這些技術的應用不僅降低了成本，還創造了新的商業機遇。企業需要建立完善的數字戰略以適應不斷變化的市場環境。",
    
    "可再生能源產業正面臨前所未有的發展機遇。太陽能和風能技術成本的下降使其越來越具有競爭力。政府政策支持和企業投資的增加加速了能源結構的調整。這種轉變既應對了環境挑戰，也為經濟發展帶來了新的增長點。",
    
    "網絡安全已成為企業信息管理的核心要素。隨著威脅的不斷演變，組織必須採取全面的安全措施保護系統和數據。實施多因素認證、加密協議和定期安全審計有助於降低潛在風險。員工安全意識培訓是維持強大安全防護的關鍵。",
]


def create_dataset(output_path: str = 'data/training_data.csv', language: str = 'english'):
    """
    建立訓練數據集
    
    Args:
        output_path: 輸出 CSV 檔案路徑
        language: 'english' 或 'chinese'
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    if language == 'english':
        human_texts = HUMAN_SAMPLES
        ai_texts = AI_SAMPLES
    else:
        human_texts = HUMAN_SAMPLES_CN
        ai_texts = AI_SAMPLES_CN
    
    data = []
    
    # 添加 Human 樣本
    for text in human_texts:
        data.append({'text': text, 'label': 0})  # 0 = Human
    
    # 添加 AI 樣本
    for text in ai_texts:
        data.append({'text': text, 'label': 1})  # 1 = AI
    
    # 寫入 CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['text', 'label'])
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Dataset created: {output_path}")
    print(f"Total samples: {len(data)} (Human: {len(human_texts)}, AI: {len(ai_texts)})")


def create_json_dataset(output_path: str = 'data/training_data.json', language: str = 'english'):
    """
    建立 JSON 格式的數據集
    
    Args:
        output_path: 輸出 JSON 檔案路徑
        language: 'english' 或 'chinese'
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    if language == 'english':
        human_texts = HUMAN_SAMPLES
        ai_texts = AI_SAMPLES
    else:
        human_texts = HUMAN_SAMPLES_CN
        ai_texts = AI_SAMPLES_CN
    
    data = {
        'human': [{'text': text, 'label': 0} for text in human_texts],
        'ai': [{'text': text, 'label': 1} for text in ai_texts],
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"JSON dataset created: {output_path}")


def load_dataset(dataset_path: str) -> List[Dict]:
    """
    載入數據集
    
    Args:
        dataset_path: 數據集檔案路徑
        
    Returns:
        數據列表
    """
    data = []
    
    if dataset_path.endswith('.csv'):
        with open(dataset_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    'text': row['text'],
                    'label': int(row['label'])
                })
    elif dataset_path.endswith('.json'):
        with open(dataset_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            if isinstance(raw_data, dict):
                data = raw_data.get('human', []) + raw_data.get('ai', [])
            else:
                data = raw_data
    
    return data


if __name__ == "__main__":
    # 建立英文數據集
    create_dataset('data/training_data_en.csv', language='english')
    create_json_dataset('data/training_data_en.json', language='english')
    
    # 建立中文數據集
    create_dataset('data/training_data_cn.csv', language='chinese')
    create_json_dataset('data/training_data_cn.json', language='chinese')
    
    # 測試載入
    data = load_dataset('data/training_data_en.csv')
    print(f"\nLoaded {len(data)} samples from CSV")
