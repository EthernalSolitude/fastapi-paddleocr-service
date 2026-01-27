import requests
import os

URL = "http://127.0.0.1:8000/api/process"
FILE_PATH = "test_doc.pdf"  
OUTPUT_FILE = "result_from_api.pdf"

if not os.path.exists(FILE_PATH):
    print(f" Ошибка: Файл '{FILE_PATH}' не найден!")
    exit()


files = {
    'file': open(FILE_PATH, 'rb')  
}

print(f"Отправка {FILE_PATH} на сервер...")

try:
    #POST запрос
    # stream=True нужен, чтобы не грузить RAM
    response = requests.post(URL, files=files, stream=True)

    #Проверка ответа
    if response.status_code == 200:
        # Сохраняем полученный PDF
        with open(OUTPUT_FILE, 'wb') as f: 
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Результат сохранен в: {OUTPUT_FILE}")
    else:
        print(f"Ошибка сервера: {response.status_code}")
        print("Детали:", response.text)

except Exception as e:
    print(f"Ошибка соединения: {e}")

finally:
    # Всегда закрываем файл
    files['file'].close()
