FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=fitness_club.settings.prod

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p logs media staticfiles static

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and create superuser (optional)
RUN python manage.py migrate || true

EXPOSE 8000

CMD ["gunicorn", "fitness_club.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]