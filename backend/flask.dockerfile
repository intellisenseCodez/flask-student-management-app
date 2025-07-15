# Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py
    

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .


# Ensure wait script is executable
RUN chmod +x ./wait-for-mysql.sh

# Expose the application port
EXPOSE 8080

# Default command (runs wait + db upgrade + flask server)
CMD /wait-for-mysql.sh && flask db upgrade && gunicorn app:app -b 0.0.0.0:8080 --workers 4 --timeout 120


