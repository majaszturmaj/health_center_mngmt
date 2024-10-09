import os

class Config:
    # Ustawienia bazy danych
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ordynator:root@localhost/psychiatric_hospital'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Klucz do sesji
    SECRET_KEY = os.urandom(24)

