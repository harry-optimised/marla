# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Collect static files
RUN python marla/manage.py collectstatic --no-input

# Add and run as non-root user
RUN adduser --disabled-password myuser
USER myuser

# Run the application
WORKDIR /code/marla
CMD gunicorn marla.wsgi:application --bind 0.0.0.0:8000
