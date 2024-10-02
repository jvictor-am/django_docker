# Use an official Python runtime as a parent image
FROM python:3.12.5-alpine3.20

# Install system dependencies
RUN apk add --no-cache \
        gcc \
        musl-dev \
        postgresql-dev \
        && pip install poetry

# Set the working directory
WORKDIR /usr/src/app

# Copy pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* ./

# Install the dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the current directory into the container
COPY . .


# Copy the wait script
COPY wait_for_db.sh /usr/src/app/wait_for_db.sh
RUN chmod +x /usr/src/app/wait_for_db.sh

# Expose the port for Django
EXPOSE 8080

# Define an environment variable for the superuser creation
ENV DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_PASSWORD=adminpassword \
    DJANGO_SUPERUSER_EMAIL=admin@example.com

# Run migrations, create superuser, and start the Django server
CMD ["sh", "-c", "./wait_for_db.sh && \
    poetry run python manage.py makemigrations && \
    poetry run python manage.py migrate && \
    poetry run python manage.py create_superuser && \
    poetry run python manage.py runserver 0.0.0.0:8080"]
    
    # poetry run python manage.py load_data && \
