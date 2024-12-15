from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 啟用 CORS

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
        data["description"].append(paragraph.get_text(strip=True))

    details = h2.find_next('details')
    if details:
        h3 = details.find('h3')
        if h3:
            data["sub_title"] = h3.get_text(strip=True)
        ul = details.find('ul')
        if ul:
            data["side_effects"] = [li.get_text(strip=True) for li in ul.find_all('li')]

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)