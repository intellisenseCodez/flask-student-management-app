# Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install mysqladmin
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .


# Copy the MySQL wait script into the container
# COPY wait-for-mysql.sh .

# Make the wait script executable
# RUN chmod +x wait-for-mysql.sh

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8080
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the application port
EXPOSE 8080


# Run wait-for-mysql, apply migrations, then start Flask server
CMD ["sh", "-c", "./wait-for-mysql.sh && flask db upgrade && flask run --host=0.0.0.0 --port=8080"]



