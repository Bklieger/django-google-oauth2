# Djgoprod App

In this folder, the main app-wide configuration settings are applied.

Files with code:
- global_utils.py: Three global utils used for printing green, yellow, and red statements in the error and warning report.
- settings.py: Global Django configuration for the application settings.
- urls.py: Set the urls for the application which include the accounts (login, logout), allauth (other auth endpoints), and admin (Django built-in admin).
- wsgi.py: Web Server Gateway Interface (WSGI) for production deployments.

## Details

The djgoprod app defines the main configuration settings for the djoprod application. The settings.py file contains most of the code, which contains comprehensive error and warning statements as well as changes in behavior based upon deployment environments.

## Environment Variables

Environment Variables:  
    - GOOGLE_CLIENT_ID: A string representing the Google OAuth2 client ID.  
        [Environment variable in: local, development, production]  
        
    - GOOGLE_CLIENT_SECRET: A string representing the Google OAuth2 client secret.  
        [Environment variable in: local, development, production]  

    - DJANGO_SETTINGS_MODULE: Required for running, always djgoprod.settings  
        [Environment variable in: local, development, production (all)]  

    - DEPLOYMENT: A string representing the deployment environment.
        [Options: local, development, production]

    - SECRET_KEY: A secret key for the Django project.
        [Environment variable in: development, production]

    - ALLOWED_HOSTS: A list of strings representing the allowed hosts.
        [Environment variable in: development, production]

    - PSQL_DATABASE_URL: A string representing the database URL.
        [Environment variable in: development, production]

    - LOCAL_SQLITE: A string representing the name of the local SQLite database (without .sqlite3 extension).
        [Environment variable in: local]