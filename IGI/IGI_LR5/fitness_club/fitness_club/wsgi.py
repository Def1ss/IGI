import os
from django.core.wsgi import get_wsgi_application

# Default settings environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_club.settings.prod')

application = get_wsgi_application()
