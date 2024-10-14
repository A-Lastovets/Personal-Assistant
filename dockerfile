# Використовуємо образ Python
FROM python:3.12.2-bookworm

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файли проекту в контейнер
COPY . .

# Встановлюємо залежності
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Виконуємо команду збору статичних файлів
RUN python personal_assistant/manage.py collectstatic

# Виставляємо порт
EXPOSE 8000

# Gunicorn для стабільного продакшн-середовища
#Коли Gunicorn запускається, він створює кілька воркерів, щоб паралельно обробляти запити
CMD ["gunicorn", "--workers", "9", "--bind", "0.0.0.0:8000", "personal_assistant.wsgi:application"]
