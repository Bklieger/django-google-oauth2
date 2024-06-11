"""
urls.py file for djgoprod app.

Author(s): Benjamin Klieger
Date: 2024-06-01
"""

# Import Django Modules
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from .views import welcome_view

# Url Patterns
urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('accounts/', include('accounts.urls')), # Include accounts app urls
    path('admin/', admin.site.urls), # Include admin urls
    path('allauth/', include('allauth.urls')), # Include allauth urls
    # path('allauth/', include('allauth.socialaccount.providers.google.urls')), # You can use this instead of include('allauth.urls') to only enable Google OAuth allauth endpoints.
]
