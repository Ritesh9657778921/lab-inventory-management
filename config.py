import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALERT_THRESHOLD = 5  # Set the threshold for low stock alerts
    EXPIRY_ALERT_DAYS = 30  # Days before expiry to trigger an alert