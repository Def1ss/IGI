import os
from django.core.wsgi import get_wsgi_application

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'fitness_club.settings.dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()