# Accounts App

This app and folder holds the account-related functionality.

Files with code:
- templates/login.html: Basic login frontend for testing Google OAuth.
- admin.py: Register CustomUser model for admin dashboard.
- apps.py: Register accounts as Django app.
- models.py: Create CustomUser model extending AbstractUser. This allows you to add new fields and logic to your user object. 
- urls.py: Create the Google OAuth2, frontend login, and backend logout endpoints.
- views.py: Functionality defined for the frontend login and backend logout endpoints.

## Details

The accounts app handles authentication and user accounts for the Django app. Specifically, CustomUser is defined in models.py, and login/logout urls are defined. Google OAuth2 is currently the login method.