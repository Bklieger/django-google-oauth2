"""
wsgi.py file for djgoprod app.

WSGI config for djgoprod project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/

Author(s): Benjamin Klieger
Date: 2024-06-01
"""

# Import OS for environment variables
import os

# Import Django libraries
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djgoprod.settings')

application = get_wsgi_application()