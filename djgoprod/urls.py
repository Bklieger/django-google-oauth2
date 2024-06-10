"""
urls.py file for djgoprod app.

Author(s): Benjamin Klieger
Date: 2024-06-01
"""

# Import Django Modules
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

# Url Patterns
urlpatterns = [
    path('accounts/', include('accounts.urls')), # Include accounts app urls
    path('admin/', admin.site.urls), # Include admin urls
    path('allauth/', include('allauth.urls')), # Include allauth urls
]
