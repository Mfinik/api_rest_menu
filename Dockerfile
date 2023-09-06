# Используем официальный образ Python 3.11
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y libpq-dev

# Устанавливаем зависимости
RUN pip install poetry

# Создаем и устанавливаем пользователь app
RUN useradd -ms /bin/bash app
#USER app
WORKDIR /home/app
COPY pyproject.toml poetry.lock /home/app/
RUN poetry install --no-dev --no-interaction --no-ansi

# Копируем исходники приложения в контейнер
COPY --chown=app:app . .

# Запускаем приложение
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
