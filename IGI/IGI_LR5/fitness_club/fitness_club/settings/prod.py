import os
from .base import *

DEBUG = False

# Production DB configuration
DB_NAME = os.environ.get('DB_NAME', 'fitness_db')
DB_USER = os.environ.get('DB_USER', 'fitness_admin')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'secure_strength_pass')
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', '5432')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}
