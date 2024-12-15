from googletrans import Translator

# 建立翻譯器物件
translator = Translator()

# 翻譯英文到中文
result = translator.translate('Hello, how are you?', src='en', dest='zh-TW')

# 顯示翻譯結果
print(f'原文: Hello, how are you?')
print(f'翻譯後: {result.text}')