# 📘 Project: Building a Three-Tier Architecture with Flask, MySQL, and Next.js in Docker

## 📌 Overview
This project demonstrates a three-tier architecture using:
- **Backend**: Flask (Python web framework), SQLAlchemy (ORM)
- **Database**: MySQL (database)
- **Frontend**: Next.js (React-based SSR framework)

It showcases full-stack application development, container orchestration, and production-aligned patterns like service health checks, environment-based configuration, and database migrations.

## 🎯 Objectives
- Build a clean separation of concerns using a three-tier model.
- Implement Flask APIs to handle core business logic and persistence.
- Use MySQL as a relational database backend.
- Serve a modern Next.js frontend.
- Deploy all services using Docker Compose.
- Add production-aware patterns like health checks, entrypoint wait scripts, and environment management.

## 📐 Architecture
Here's a simplified architecture diagram:
```bash
flask-student-management-app
backend/
    ├── app/
    │   ├── models/           # SQLAlchemy models for Student, Course, Enrollment
    │   └── routes/           # Flask Blueprints (API endpoints)
    ├── migrations/           # Flask-Migrate scripts
    ├── .dockerignore         # dockerignore file
    ├── flask.dockerfile      # Dockerfile for Flask service
    ├── main.py               # App entrypoint
    ├── requirements.txt      # requirements for Flask app
    ├── wait-for-mysql.sh     # Wait script for MySQL readiness
frontend/
    ├── (Your Next.js app here)
.gitignore
compose.yml               # Docker Compose for all services
.env                      # Environment variables
README.md
```

## 🧪 Running the Flask Backend Locally
This section guides you through setting up and running the Flask backend locally on your machine for development and testing purposes.

1. Clone the Repository
```bash
git clone https://github.com/intellisenseCodez/flask-student-management-app.git
cd flask-student-management-app
```

2. Configure Flask Environment Variables
Inside the `backend/` directory, create a `.flaskenv` file:
```bash
cd backend
touch .flaskenv
```
Add the following content to `.flaskenv`:
```bash
# Flask Environment Configuration
FLASK_APP=main.py
FLASK_ENV=development
FLASK_RUN_PORT=8080
FLASK_RUN_HOST=127.0.0.1
DEBUG=1

# SQLAlchemy connection URI 
DATABASE_URL=mysql+pymysql://root:your-password@localhost:3306/student_db
```

- Replace `your-password` with your actual MySQL root password.
- `.flaskenv` is automatically used by Flask when running locally if you have the python-dotenv package installed.

`Note:` Ensure that MySQL Server is installed and running on your local system. You can download it here: [MySQL Download](https://dev.mysql.com/downloads/).

3. Create a MySQL Database
You can create the database using MySQL Workbench or the MySQL CLI:
```bash
CREATE DATABASE IF NOT EXISTS student_db;
```

4. Set Up a Python Virtual Environment
From inside the `backend/` directory:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # For Linux/macOS
# OR
venv\Scripts\activate     # For Windows
```

`Reference`: Learn more about Python virtual environments [page](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).

5. Install Python Dependencies
After activating the virtual environment, install the required packages:
```bash
pip install -r requirements.txt
```

5. Run Database Migrations
Use `Flask-Migrate` to create the tables in your student_db:
```bash
flask db upgrade
```
`Reference`: Learn more about Flask Migration [page](https://flask-migrate.readthedocs.io/en/latest/).

![database runing](./images/database.png)

6. Start the Flask Development Server
Finally, run the application:
```bash
flask run
```
![application runing](./images/flask-running.png)

By default, it will be available at:
🔗 http://127.0.0.1:8080

## 🐳 Dockerizing the Flask Backend
### 1. Dockerfile:
In `backend/`, we have a file named flask.dockerfile:

```bash
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
COPY wait-for-mysql.sh .

# Make the wait script executable
RUN chmod +x wait-for-mysql.sh

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8080
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the application port
EXPOSE 8080


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
COPY wait-for-mysql.sh .

# Make the wait script executable
RUN chmod +x wait-for-mysql.sh

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8080
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the application port
EXPOSE 8080


# Run wait-for-mysql, apply migrations, then start Flask server
CMD ["sh", "-c", "./wait-for-mysql.sh && flask db upgrade && flask run --host=0.0.0.0 --port=8080"]
```

### 2. MySQL Wait Script
we also have `backend/wait-for-mysql.sh`:
The `wait-for-mysql.sh` script ensures that your Flask backend only starts after the MySQL database is fully up and ready to accept connections.

```bash
#!/bin/bash

echo "Waiting for MySQL to become healthy..."

until mysqladmin ping -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
    sleep 2
done

echo "MySQL is up!"
exec "$@"
```

### 2. Define Environment Variables
Create a .env file in the project root:

```bash
# MySQL Environment Variables
MYSQL_HOST="database" 
MYSQL_ROOT_PASSWORD="rootpassword"
MYSQL_DATABASE="studentdb"
MYSQL_USER="testuser"
MYSQL_PASSWORD="testpassword"

# SQLAlchemy connection URI 
DATABASE_URL=mysql+pymysql://testuser:testpassword@database:3306/student_db

# dockerhub username
DOCKERHUB_USERNAME=your-username
```

### 4. Docker Compose
In your root directory we have compose.yml:

```bash
services:

  # backend service
  backend:
    container_name: flask-student-api
    restart: always
    image: ${DOCKERHUB_USERNAME}/flask-student-api:v1.0
    build:
      context: ./backend
      dockerfile: flask.dockerfile
    ports:
      - 8080:8080
    env_file: ".env"
    environment:
      - DATABASE_URL=mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@database:3306/${MYSQL_DATABASE}
    depends_on:
      - database


  # database service
  database:
    container_name: mysql-database
    image: mysql:5.7
    env_file: ".env"
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
    ports:
      - 3307:3306
    volumes:
      - mysql_data:/var/lib/mysql
  

  # frontend service



volumes:
  mysql_data: {}
```


### 5. 🚀 Run Your Backend with Docker
Ensure you are in the root project:
```bash
# run in non-detached mode
docker-compose up --build 
OR
# run in detached mode
docker-compose up -d --build
```
Once the services are up, your Flask API should be available at:
🔗 http://localhost:8080

![docker-compose runing](./images/docker-output-1.png)

![docker-compose runing](./images/docker-output-2.png)

✅ Testing the API
🧪 Testing the API Using Postman
Once your Flask backend is up and running (either locally or via Docker), you can use [Postman]("https://www.postman.com/") — a popular API testing tool — to interact with your API endpoints.

## Endpoints to Test
| Method    | Endpoint    | Description    |
|-----------|-------------|----------------|
| POST	 | `/api/v1.0/student/create`  | Create a new student  |
| GET	 | `/api/v1.0/students/all`  | Retrieve all students  |
| GET	 | `/api/v1.0/students/<student-id>`  | Retrieve student by ID  |
| GET	 | `/api/v1.0/students/by-course?course_title="your course"`  | Retrieve students by course title  |
| PUT	 | `/api/v1.0/students/<student-id>`  | Update student by ID  |
| DELETE	 | `/api/v1.0/students/<student-id>`  | Delete student by ID  |
| POST	 | `/api/v1.0/course/create`  | Create a new course  |
| GET	 | `/api/v1.0/course/all`  | Retrieve all courses  |
| GET	 | `/api/v1.0/course/<course-id>`  | Retrieve course by ID  |
| PUT	 | `/api/v1.0/courses/<course-id>`  | Update course by ID  |
| DELETE	 | `/api/v1.0/courses/<course-id>`  | Delete course by ID  |
| POST	 | `/api/v1.0/course/add/<course-id>`  | Enroll student for a course  |
| GET	 | `/api/v1.0/students/<student-id>/courses`  | Retrieve all enrolled courses by student  |


![postman ](./images/postman.png)



## 🙌 Credits
This project was built for learning and demonstration purposes. Inspired by real-world backend system design and frontend integration practices.

