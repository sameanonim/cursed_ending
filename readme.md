# Дипломный проект: Сайт медицинской компании

## Настройка и запуск приложения

1. **Настройка виртуального окружения и установка зависимостей:**

    - Команда для Windows:
        ```
        python -m venv venv
        venv\Scripts\activate
        pip install -r requirement.txt
        ```

    - Команда для Unix:
        ```
        python3 -m venv venv
        source venv/bin/activate 
        pip install -r requirement.txt
        ```

2. **Запуск Redis:**

    - Redis официально не поддерживается в Windows, поэтому вам нужно установить WSL2 и Ubuntu. Подробности смотрите [здесь](https://redis.io/docs/getting-started/installation/install-redis-on-windows/). Затем выполните следующие команды:
        ```
        sudo apt-get update
        sudo service redis-server start
        redis-cli
        ping
        ```
      Ответом от сервиса должно быть PONG. Это означает что Redis подключен.

    - Команда для Unix:
        ```
        redis-cli
        ```

3. **Создание БД:**
    ```
    sudo -u postgres psql
    CREATE DATABASE medical;
    \q
    ```

4. **Применение миграций:**
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Заполнение моделей данными:**

    - Команда для Windows:
        ```
        python manage.py loaddata db.json  
        ```

    - Команда для Unix:
        ```
        python3 manage.py loaddata db.json
        ```

6. **Работа с переменными окружениями:** необходимо заполнить файл .env на основе .env.sample.

7. **Создание администратора (createsuperuser):** заполните поля email, PASSWORD в файле users/management/commands/csu.py.

    - Команда для Windows:
       ```
       python manage.py csu
       ```

    - Команда для Unix:
       ```
       python3 manage.py csu
       ```

8. **Запуск приложения:**

   - Команда для Windows:
      ```
      python manage.py runserver
      ```

   - Команда для Unix:
      ```
      python3 manage.py runserver
      ```

9. **Запуск Celery:**
   ```
   celery -A config worker -l info
   celery -A core beat -l INFO     
   ```

10. **Доступ к сайту:** осуществляется по IP-адресу: http://127.0.0.1:8000/  

11. **Доступ к административной панели:** http://127.0.0.1:8000/admin/