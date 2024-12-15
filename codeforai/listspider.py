import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 建立翻譯器物件
translator = Translator()

# 設定目標藥品名稱的串列
drug_names = ['aspirin', 'ibuprofen', 'acetaminophen']  # 請將藥品名稱替換為您需要查詢的名稱

# 遍歷藥品名稱串列
for drug_name in drug_names:
    print(f"Fetching data for drug: {drug_name}...")
    
    url = f'https://www.drugs.com/sfx/{drug_name}-side-effects.html'
    response = requests.get(url)
    
    # 確認請求成功
    if response.status_code == 200:
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到指定的 <h2> 標籤
        h2 = soup.find('h2', {'class': 'ddc-anchor-offset'})
        if h2:
            # 打印未翻譯的藥品名稱（即 <h2> 標籤的文本）
            print("Title:", h2.get_text(strip=True))

            # 提取該 <h2> 標籤之後的所有 <p> 標籤
            paragraphs = h2.find_all_next('p', limit=2)  # 提取接下來的兩個 <p> 標籤
            
            # 打印翻譯過的段落
            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)
                translated_text = translator.translate(text, src='en', dest='zh-tw').text
                print(translated_text)  # 輸出翻譯後的段落文本內容

            # 找到列表項目
            details = h2.find_next('details')
            if details:
                # 提取 <h3> 標題並翻譯
                h3 = details.find('h3')
                if h3:
                    translated_sub_title = translator.translate(h3.get_text(strip=True), src='en', dest='zh-tw').text
                    print("Sub Title:", translated_sub_title)

                ul = details.find('ul')
                if ul:
                    list_items = ul.find_all('li')  # 獲取所有的 <li> 項目
                    
                    # 提取並打印每個副作用，並進行翻譯
                    for item in list_items:
                        text = item.get_text(strip=True)
                        translated_side_effect = translator.translate(text, src='en', dest='zh-tw').text
                        print(translated_side_effect)  # 輸出翻譯後的副作用
        else:
            print(f"No relevant <h2> found for drug: {drug_name}")
    else:
        print(f"Failed to retrieve data for {drug_name}. Status code: {response.status_code}")
    
    print("-" * 50)  # 分隔不同藥品的輸出
