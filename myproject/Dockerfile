 FROM python:3.12

 WORKDIR /app

 # Устанавливаем зависимости
 COPY requirements.txt ./
 RUN pip install --no-cache-dir -r requirements.txt

 # Копируем код проекта
 COPY . .

 # # Собираем статику  <-- закомментировано
 # RUN mkdir -p /tmp/static_test
 # COPY ./staticfiles /tmp/static_test

 # Создаем пользователя django
 RUN adduser --disabled-password django
 USER django

 # Запускаем Gunicorn
 CMD ["gunicorn", "lms.wsgi:application", "--bind", "0.0.0.0:8000"]