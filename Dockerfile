FROM python:3.11.4

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    libgl1-mesa-glx \
    tesseract-ocr \
    tesseract-ocr-ukr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Встановлення PYTHONPATH
ENV PYTHONPATH="/app/vision_park:${PYTHONPATH}"
# Встановлення Django налаштувань
ENV DJANGO_SETTINGS_MODULE=vision_park.settings

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_URL=postgresql://postgres:1234@db:5432/vision_park_db


