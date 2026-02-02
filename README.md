# OCR Service

Веб-сервис для распознавания текста на изображениях/pdf-документах. Используется PaddleOCR V3 (Mobile версия). Работает на CPU.

---

## Установка и запуск

### Способ 1: Локальная установка

Самый простой способ для разработки и тестирования.

**Для это требуется:**
- Python 3.10+
- pip

**Шаги:**

```bash
#Клонируйте репозиторий
git clone https://github.com/EthernalSolitude/fastapi-paddleocr-service.git

# Перейдите в папку проекта
cd fastapi-paddleocr-service

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python run.py
```

Сервис запустится на `http://localhost:8000`

---

### Способ 2: Использование готового Docker образа

Образ уже содержит необходимые модели и зависимости.

**Требования:**
- Docker Desktop (Windows/Mac) или Docker Engine (Linux)

**Первый запуск:**

```bash
docker run -d -p 8000:8000 --name my-ocr cvenjoyer/ocr-service:latest
```

**Последующие запуски:**

Через Docker Desktop:
1. Откройте Docker Desktop
2. Перейдите на вкладку "Containers"
3. Найдите контейнер `my-ocr`
4. Нажмите кнопку Play (запуск)

Или через терминал:

```bash
docker start my-ocr
```

**Остановка:**

```bash
docker stop my-ocr
```

---

## Использование приложения

### Веб-интерфейс (Swagger UI)

### Пошаговая инструкция

**Шаг 1:** Откройте http://localhost:8000/docs

**Шаг 2:** Найдите эндпоинт `POST /api/process` (зеленая кнопка)

**Шаг 3:** Нажмите на эндпоинт, чтобы развернуть его

**Шаг 4:** Нажмите кнопку "Try it out"

**Шаг 5:** Нажмите кнопку "Choose File" и выберите изображение с текстом

**Шаг 6:** Нажмите "Execute"

**Шаг 7:** После обработки перейдите чуть ниже в раздел server response.

**Шаг 8:** В поле Response body появится ссылка на скачивание файла с результатом (Download file) и текстовый json.

## Технические детали

### Модели

Используется **PaddleOCR mobile версия**:
- **Детекция текста**: PP-OCRv3_mobile_det 
- **Распознавание текста**: PP-OCRv3_mobile_rec 

## Структура файлов

```
fastapi-paddleocr-service/
├── app/                       # Весь исходный код приложения
│   ├── __init__.py
│   ├── main.py                # Точка входа FastAPI (создание app)
│   ├── api/                   # API роуты (эндпоинты)
│   │   ├── __init__.py
│   │   └── routes.py          
│   ├── core/                  # Настройки и конфиги
│   │   ├── __init__.py
│   │   └── config.py          # Переменные окружения, пути к моделям
│   ├── services/              # Сервисная логика приложения
│   │   ├── __init__.py
│   │   ├── ocr.py             # Класс PaddleOCRModel (логика распознавания)
│   │   └── visualizer.py      # Рисование bounding boxes на фото
│   └── utils/                 # Вспомогательные функции
│       ├── __init__.py
│       └── file_utils.py      # Работа с файлами, конвертация PDF
├── assets/                    
│   └── Arial.ttf       
├── Dockerfile                 # Инструкция сборки
├── download_model.py          # Скрипт для предзагрузки моделей (для Docker)
├── requirements.txt           # Список зависимостей
├── run.py                     # Скрипт запуска (entry point)
├──test_api.py                 # тест эндпоинтов
```

## Docker Hub

Образ доступен на Docker Hub:

[https://hub.docker.com/r/cvenjoyer](https://hub.docker.com/repositories/cvenjoyer)

```bash
docker pull cvenjoyer/ocr-service:latest
```

