# Домашняя работа №30 (DRF) - LMS API

API для системы управления обучением (LMS), разработанный с использованием Django REST Framework (DRF).

## Инструкция по развертыванию и запуску проекта

### Способ 1: Развертывание и запуск проекта с помощью Docker Compose (Рекомендуемый)

Этот раздел описывает, как развернуть и запустить проект, используя Docker и Docker Compose. Это **рекомендуемый способ** для наиболее простой и воспроизводимой установки.

#### Предварительные требования

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

#### Инструкция по установке и запуску

1.  **Клонирование проекта:**

    ```bash
    git clone <URL_вашего_репозитория>
    cd <имя_папки_проекта>
    ```

2.  **Создание файла `.env`:**

    *   Скопируйте файл `.env.example` в `.env`:

        ```bash
        cp .env.example .env
        ```
    *   Отредактируйте файл `.env` и внесите необходимые настройки.  **Подробное описание переменных окружения см. ниже.**

3.  **Запуск проекта с помощью Docker Compose:**

    ```bash
    docker-compose up -d --build
    ```

    *   `-d`:  Запускает контейнеры в фоновом режиме (detached).
    *   `--build`: Собирает образы, если они еще не собраны или если `Dockerfile` был изменен.

4.  **Остановка проекта:**

    ```bash
    docker-compose down
    ```

    Это остановит и удалит все контейнеры, созданные `docker-compose up`.

### Способ 2: Локальная установка (Для разработки и тестирования)

Этот раздел описывает, как установить и запустить проект локально, без использования Docker.

#### Предварительные требования

*   Python 3.8+
*   pip
*   PostgreSQL (или другая поддерживаемая база данных)

#### Инструкция по установке и запуску

1.  **Клонирование проекта:**

    ```bash
    git clone <URL_вашего_репозитория>
    cd <имя_папки_проекта>
    ```

2.  **Создание и активация виртуального окружения:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate  # Windows
    ```

3.  **Установка зависимостей Python:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройка базы данных:**

    *   Создайте базу данных PostgreSQL (или другую, указанную в настройках).
    *   Укажите параметры подключения к базе данных в файле `.env`.  **См. описание переменных окружения ниже.**
    *   Выполните миграции Django:

        ```bash
        python manage.py migrate
        ```

5.  **Создание суперпользователя (опционально):**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Запуск сервера разработки:**

    ```bash
    python manage.py runserver
    ```

### Способ 3: Продакшен-развертывание на Yandex Cloud

Этот раздел описывает шаги по развертыванию приложения на сервере Ubuntu 22.04 в Yandex Cloud.

#### Предварительные требования

*   Аккаунт в Yandex Cloud
*   Доступ к серверу Ubuntu 22.04 по SSH

#### Инструкция по установке и запуску

1.  **Создайте сервер Ubuntu 22.04 на Yandex Cloud.**
2.  **Настройте базовые зависимости:**

    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y python3.11 python3.11-venv nginx postgresql redis
    ```

3.  **Настройте PostgreSQL:**

    *   (Укажите здесь инструкции по настройке PostgreSQL. Если у тебя есть отдельный файл с инструкциями, дай ссылку на него. Если нет, то нужно будет добавить инструкции сюда. Например:
        *   Создайте пользователя базы данных: `sudo -u postgres createuser -P <username>`
        *   Создайте базу данных: `sudo -u postgres createdb -O <username> <database_name>`
        *   Настройте доступ к базе данных в `pg_hba.conf` (если нужно).
        *   Укажите параметры подключения к базе данных в файле `.env`.)

4.  **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/ваш-репозиторий.git /home/ubuntu/lms
    ```

5.  **Настройте виртуальное окружение:**

    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

6.  **Настройте Gunicorn и Nginx:**

    *   (Здесь нужно добавить инструкции по настройке Gunicorn и Nginx.  Это будет включать:
        *   Создание файла сервиса Gunicorn (например, `/etc/systemd/system/gunicorn.service`).
        *   Создание конфигурации Nginx (например, в `/etc/nginx/sites-available/`).
        *   Включение конфигурации Nginx (создание симлинка).
        *   Перезапуск Nginx и Gunicorn.)

7.  **Создайте файл `.env` на основе `.env.example`:**

    *   Скопируйте файл `.env.example` в `/home/ubuntu/lms/.env`:
        ```bash
        cp /home/ubuntu/lms/.env.example /home/ubuntu/lms/.env
        ```
    *   Отредактируйте `/home/ubuntu/lms/.env` и внесите необходимые настройки.  **См. описание переменных окружения ниже.**

8.  **Выполните миграции Django:**

    ```bash
    python /home/ubuntu/lms/manage.py migrate
    ```

9. **Сбор статики Django:**

    ```bash
    python /home/ubuntu/lms/manage.py collectstatic
    ```

10. **Запустите сервисы:**

    ```bash
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    sudo systemctl restart nginx
    ```

## Переменные окружения

Файл `.env` содержит переменные окружения, необходимые для работы приложения. Ниже приведено описание наиболее важных переменных:

*   `SECRET_KEY`:  Секретный ключ Django.  **Важно! Сгенерируйте случайный и уникальный ключ для production.**
*   `DEBUG`:  Включить/выключить режим отладки (True/False). **В production должен быть False.**
*   `DATABASE_URL`: URL для подключения к базе данных.  Пример: `postgres://user:password@host:port/database`
*   `ALLOWED_HOSTS`:  Список разрешенных хостов для Django.  В production укажите доменные имена вашего сервера. Пример: `["example.com", "www.example.com"]`
*   `EMAIL_HOST`:  Хост SMTP-сервера для отправки электронной почты.
*   `EMAIL_PORT`:  Порт SMTP-сервера.
*   `EMAIL_HOST_USER`:  Имя пользователя для SMTP-сервера.
*   `EMAIL_HOST_PASSWORD`:  Пароль для SMTP-сервера.
*   `DEFAULT_FROM_EMAIL`:  Адрес электронной почты, который будет использоваться в качестве отправителя.
*   `REDIS_URL`: URL для подключения к Redis (если используется Celery). Пример: `redis://host:port/0`
*   `CELERY_BROKER_URL`: URL брокера сообщений Celery (обычно совпадает с `REDIS_URL`).
*   `CELERY_RESULT_BACKEND`: URL для хранения результатов задач Celery (обычно совпадает с `REDIS_URL`).

## Дополнительная информация

*   **API Documentation:**  Документация к API будет доступна по адресу `/swagger/` после запуска приложения.
*   **Администрирование:**  Панель администрирования Django будет доступна по адресу `/admin/` (если создан суперпользователь).

## Известные проблемы

*   (Здесь можно перечислить известные проблемы и способы их решения)

## Contributing

Если вы хотите внести вклад в проект, пожалуйста, создайте pull request с описанием изменений.