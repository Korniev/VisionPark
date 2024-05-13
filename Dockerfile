# Використання офіційного образу Python як базового
FROM python:3.11.4

# Задання змінної середовища, щоб вивід Python не був буферизований
ENV PYTHONUNBUFFERED=1

# Встановлення необхідних пакетів
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    libgl1-mesa-glx \
    tesseract-ocr \
    tesseract-ocr-ukr \
    && rm -rf /var/lib/apt/lists/*

# Встановлення робочої директорії у контейнері
WORKDIR /app

# Копіювання файлу залежностей у контейнер
COPY requirements.txt requirements.txt

# Встановлення Python бібліотек без кешування
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання всіх інших файлів проекту у контейнер
COPY . .

# Задання змінної середовища для бази даних
ENV DATABASE_URL=postgresql://postgres:1234@db:5432/vision_park_db
