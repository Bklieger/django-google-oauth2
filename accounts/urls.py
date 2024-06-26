"""
Urls.py file for accounts app.

Author(s): Benjamin Klieger
Date: 2024-06-01
"""

# Import required libraries for Google OAuth
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# Create a GoogleLogin class to handle the Google OAuth login
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:8000/accounts/dj-rest-auth/google/'
    client_class = OAuth2Client

# Import required libraries for settings urls
from django.urls import path
from . import views

# Urls for accounts app
urlpatterns = [
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'), # Google OAuth login
    path('login/', views.custom_google_login, name='login'), # Custom login page
    path('logout/', views.custom_logout, name='logout'), # Custom logout page
    path('check-auth/', views.check_auth, name='check_auth'), # Check auth status
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'), # Get CSRF token
]
