FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY download_model.py .
RUN python download_model.py && rm download_model.py

COPY . .

ENV CUDA_VISIBLE_DEVICES=""
ENV PADDLE_NO_GPU="1"

EXPOSE 8000

CMD ["python", "run.py"]
