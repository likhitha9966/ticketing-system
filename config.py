import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # Change this in production!
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysql://root:Likhitha%4069@localhost/tic'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # You might want to store your database credentials in a .env file and load them
    # using python-dotenv for production, but for local testing, this is fine.