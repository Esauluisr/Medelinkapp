import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/medelinkapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

