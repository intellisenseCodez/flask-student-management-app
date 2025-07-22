import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from app.routes.metrics_api import setup_metrics


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") # load SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app) # cross-origin request security

db = SQLAlchemy(app)
migrate = Migrate(app, db)
setup_metrics(app)


from app.models import student, course, enrollment
from app.routes import student_api, course_api, metrics_api
