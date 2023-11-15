FROM tiangolo/uvicorn-gunicorn:python3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Копируем зависимости и файлы внутрь контейнера
COPY . /app

# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["bash", "-c", "sleep 5 && uvicorn main:app --host 0.0.0.0 --port 8000"]
