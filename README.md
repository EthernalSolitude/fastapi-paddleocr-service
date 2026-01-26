# OCR Service

Веб-сервис для распознавания текста на изображениях/pdf-документах. Используется PaddleOCR (Mobile версия). Работает на CPU.

---

## Установка и запуск

### Способ 1: Локальная установка (без Docker)

Самый простой способ для разработки и тестирования.

**Для это требуется:**
- Python 3.10+
- pip

**Шаги:**

```bash
# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python run.py
```

Сервис запустится на `http://localhost:8000`

---

### Способ 2: Использование готового Docker образа

Самый быстрый способ. Образ уже содержит необходимые модели и зависимости.

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

### Способ 3: Собственная сборка Docker образа

Используйте, если хотите модифицировать код или собрать с другими параметрами.

**Шаги:**

```bash
# Клонируйте репозиторий
git clone https://github.com/EthernalSolitude/fastapi-paddleocr-service.git
cd ocr_service

# Соберите образ
docker build -t ocr-service:latest .

# Запустите контейнер
docker run -d -p 8000:8000 --name my-ocr ocr-service:latest
```

Первая сборка может занять 3-5 минут.

---

## Использование приложения

### Веб-интерфейс (Swagger UI)

Откройте браузер:

```
http://localhost:8000/docs
```

Вы увидите интерактивный интерфейс со всеми доступными функциями.

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
- **Детекция текста**: PP-OCRv5_mobile_det 
- **Распознавание текста**: PP-OCRv5_mobile_rec 

## Структура файлов

```
fastapi-paddleocr-service/
├── app/                       # Весь исходный код приложения
│   ├── __init__.py
│   ├── main.py                # Точка входа FastAPI (создание app)
│   ├── api/                   # API роуты (эндпоинты)
│   │   ├── __init__.py
│   │   └── routes.py          # /ocr/predict и другие
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
├── tests/                     # Тесты
│   ├── __init__.py
│   └── test_api.py            # Тест эндпоинтов
├── Dockerfile                 # Инструкция сборки
├── download_model.py          # Скрипт для предзагрузки моделей (для Docker)
├── requirements.txt           # Список зависимостей
└── run.py                     # Скрипт запуска (entry point)

```

## Docker Hub

Образ доступен на Docker Hub:

[https://hub.docker.com/r/cvenjoyer](https://hub.docker.com/repositories/cvenjoyer)

```bash
docker pull cvenjoyer/ocr-service:latest
```

