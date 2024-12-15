from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from googletrans import Translator

app = Flask(__name__)
CORS(app)  # 啟用 CORS

# 建立翻譯器物件
translator = Translator()

@app.route('/drug-side-effects', methods=['GET'])
def get_side_effects():
    drug_name = request.args.get('query')  # 獲取 query 參數
    if not drug_name:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    print(f"Searching for side effects of: {drug_name}")  # 打印出藥品名稱

    url = f'https://www.drugs.com/sfx/{drug_name}-side-effects.html'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": f"Failed to retrieve data for {drug_name}. Status code: {response.status_code}"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    h2 = soup.find('h2', {'class': 'ddc-anchor-offset'})

    if not h2:
        return jsonify({"error": "No side effects information found."}), 404

    # 提取副作用數據
    data = {"drug_name": drug_name, "title": h2.get_text(strip=True), "description": []}
    paragraphs = h2.find_all_next('p', limit=2)
    for paragraph in paragraphs:
        # 翻譯每個段落並加入描述，但保留藥名
        text = paragraph.get_text(strip=True)
        translated_text = translator.translate(text.replace(drug_name, f"[[{drug_name}]]"), src='en', dest='zh-tw').text
        # 恢復藥名原始格式
        translated_text = translated_text.replace(f"[[{drug_name}]]", drug_name)
        data["description"].append(translated_text)

    details = h2.find_next('details')
    if details:
        h3 = details.find('h3')
        if h3:
            # 翻譯副標題，但保留藥名
            text = h3.get_text(strip=True)
            translated_text = translator.translate(text.replace(drug_name, f"[[{drug_name}]]"), src='en', dest='zh-tw').text
            data["sub_title"] = translated_text.replace(f"[[{drug_name}]]", drug_name)
        ul = details.find('ul')
        if ul:
            # 翻譯副作用清單，但保留藥名
            data["side_effects"] = [
                translator.translate(li.get_text(strip=True).replace(drug_name, f"[[{drug_name}]]"), src='en', dest='zh-tw').text.replace(f"[[{drug_name}]]", drug_name)
                for li in ul.find_all('li')
            ]

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
