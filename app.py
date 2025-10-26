import pymysql
pymysql.install_as_MySQLdb()

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config # Import your Config class

app = Flask(__name__)
app.config['SECRET_KEY'] = '502e9bb0bea563d9ad06f5df2a86eaf1' # Make sure you have a secret key

# --- Add this database configuration ---
# This is for MySQL with PyMySQL as the driver
# Replace 'user', 'password', 'host', 'port', and 'database_name' with your actual MySQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Likhitha%4069@localhost:3306/ticketing_system_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended to disable this
print(f"Flask-SQLAlchemy connecting to: {app.config['SQLALCHEMY_DATABASE_URI']}")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Name of the login route function
login_manager.login_message_category = 'info'

# --- NEW ADDITION: Flask-Login User Loader ---
# It's important to import the User model AFTER db and login_manager are initialized
# but BEFORE the @login_manager.user_loader decorator is used.
from models import User # Import your User model here!

@login_manager.user_loader
def load_user(user_id):
    """
    Given a user_id, return the corresponding User object.
    This is used by Flask-Login to reload the user object from the user ID
    stored in the session.
    """
    return User.query.get(int(user_id))
# --- END NEW ADDITION ---

# Import routes here to avoid circular imports
from routes import * # This will import all routes defined in routes.py

# Create database tables if they don't exist
# You'd typically use Flask-Migrate for robust migrations in a real project
# NOTE: The 'from app import app, db' and 'from models import User, Ticket' are redundant here
# because 'app', 'db', 'User', 'Ticket' are already defined/imported in this file's scope.
# You can simplify this block.
if __name__ == '__main__':
    with app.app_context():
        print("Attempting to create all database tables...")
        # Ensure all models are imported before calling db.create_all()
        # You've already imported User, Ticket above. Make sure TicketResponse is also reachable
        # which it will be if it's in models.py and models.py is fully imported.
        db.create_all()
        print("db.create_all() executed. Check your database now.")

    app.run(debug=True)