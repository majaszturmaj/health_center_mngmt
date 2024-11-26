import os

class Config:
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ordynator:root@localhost/psychiatric_hospital'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    SECRET_KEY = os.urandom(24)

