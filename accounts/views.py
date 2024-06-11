"""
Urls.py file for accounts app.

Author(s): Benjamin Klieger
Date: 2024-06-01
"""

# Import required libraries for render, redirect, and logout
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from django.middleware.csrf import get_token


# View for logging in with google
def custom_google_login(request):
    if request.user.is_authenticated: # If the user is already logged in, redirect to "/". Note: Update "/" if is not the home page.
        return redirect("/")
    return render(request, 'login.html')

# View for logging out
def custom_logout(request):
    logout(request) # Logout the user
    return redirect("/")

# View to check auth
def check_auth(request):
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True})
    else:
        return JsonResponse({'authenticated': False}, status=403)

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})
