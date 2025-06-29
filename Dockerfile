# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd gcc postgresql-client libpq-dev && \
    apt-get clean

# Install Python dependencies
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run app
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
