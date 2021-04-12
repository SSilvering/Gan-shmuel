import os

SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask:flask@db/db'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///billing.db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask:flask@db/db'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///billing.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVER = '18.194.15.175'
STAGING_URI = f'http://{SERVER}:8081/'
PRODUCTION_URI = f'http://{SERVER}:8082/'
WEIGHT_STAGING_URI = f'http://{SERVER}:8083/'
WEIGHT_PRODUCTION_URI = f'http://{SERVER}:8084/'
TESTING_URI = f'http://{SERVER}:8085/'

WEIGHT_URI = WEIGHT_STAGING_URI
