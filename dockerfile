# Використовуємо образ Python
FROM python:3.12.2-bookworm

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файли проекту в контейнер
COPY . .

# Встановлюємо залежності
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir python-multipart

# Виставляємо порт
EXPOSE 8000

# Команда для запуску Django сервера
CMD ["python", "personal_assistant/manage.py", "runserver", "0.0.0.0:8000"]
