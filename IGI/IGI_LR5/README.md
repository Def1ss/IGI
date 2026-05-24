# Фитнес-клуб «ФОРСАЖ» (IGI LR5)

Веб-приложение на **Django** и **HTML-шаблонах** (без React/Node).

## Стек

- Django 4.2+
- PostgreSQL (Docker) / SQLite (локальная разработка)
- Gunicorn + Docker Compose

## Быстрый старт (локально)

```bash
cd fitness_club
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py load_fitness_fixtures
python manage.py createsuperuser   # опционально
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/

Тестовые клиенты из фикстур: логин `alex123a`, пароль `strength_client_pass`.

## Docker

```bash
cd fitness_club
docker compose up --build
```

Приложение: http://localhost:8000/

## Тесты

```bash
cd fitness_club
pytest
```

## Структура

- `fitness_club/` — настройки Django
- `apps/` — доменные приложения (контент, пользователи, расписание, отзывы и т.д.)
- `templates/` — HTML-шаблоны
- `static/` — CSS
- `tests/` — pytest
