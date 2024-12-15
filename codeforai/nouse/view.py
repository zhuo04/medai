import pytesseract
from PIL import Image

# 如果 Tesseract 不在你的 PATH 中，則指定執行檔的路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # 如有必要，更新此路徑

# 載入你的圖片
img = Image.open('test1.png')

# 對圖片進行 OCR 識別
text = pytesseract.image_to_string(img)
print(text)
