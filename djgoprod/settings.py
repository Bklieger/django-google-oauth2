"""
settings.py file for djgoprod app.

Author(s): Benjamin Klieger
Date: 2024-06-01
"""

# ------------- [Import Libraries] -------------

# Import the pathlib, os, warnings, and inspect libraries.
from pathlib import Path
import os
import warnings
import inspect

# Import dj_database_url for database configuration.
import dj_database_url

# Import functions from the global_utils.py file.
from .global_utils import green_success, yellow_warning, red_critical


# ------------- [Important Variables] -------------

"""
The following variables are used in the deployment process to track outcomes and context.
"""

# For use in building the deployment transcript to inform user of deployment status.
running_deployment_transcript = ""
critical_warnings_exist = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ------------- [Environment Variables] -------------

"""
The following environment variables are used for Google Oauth.

Requirements:
    - GOOGLE_CLIENT_ID: A string representing the Google Client ID.
    - GOOGLE_SECRET_KEY: A string representing the Google Secret Key.
"""

# Google Client ID
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

if GOOGLE_CLIENT_ID==None:
    running_deployment_transcript+= red_critical(f'[Critical] GOOGLE_CLIENT_ID environment variable not set. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True

elif len(GOOGLE_CLIENT_ID)<3:
    running_deployment_transcript+= red_critical(f'[Critical] GOOGLE_CLIENT_ID environment variable is likely invalid (<3 chars). (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True

# Google Secret Key
GOOGLE_SECRET_KEY = os.environ.get("GOOGLE_SECRET_KEY")

if GOOGLE_SECRET_KEY==None:
    running_deployment_transcript+= red_critical(f'[Critical] GOOGLE_SECRET_KEY environment variable not set. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True

elif len(GOOGLE_SECRET_KEY)<3:
    running_deployment_transcript+= red_critical(f'[Critical] GOOGLE_SECRET_KEY environment variable is likely invalid (<3 chars). (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True


# ------------- [Environment Variables for Django App] -------------

"""
Set the deployment environment by setting the DEPLOYMENT environment variable.
The default is 'local' if the DEPLOYMENT environment variable is not set.

Options:
    - local: For local development with debugging.
    - development: Tests code in conditions near identical to production. 
        Everything is identical to production except what is required to host locally.
    - production: Production environment for beta testing and release.
"""

#Set the deployment environment.
DEPLOYMENT = os.environ.get('DEPLOYMENT')

# Make deployment environment all lowercase.
if DEPLOYMENT != None:
    DEPLOYMENT = DEPLOYMENT.lower()

# Check that the deployment environment is valid. Otherwise, set it to 'local' and warn the user.
if DEPLOYMENT != 'production' and DEPLOYMENT != 'development' and DEPLOYMENT != 'local':
    DEPLOYMENT = 'local'
    running_deployment_transcript+= red_critical(f'[Critical] DEPLOYMENT environment variable not set. Defaulting to {DEPLOYMENT}. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True

# Set the deployment transcript.
running_deployment_transcript+= f'\n [Logging] Running in {DEPLOYMENT}. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n'


"""
Set the secret_key and allowed hosts based on the 
deployment environment and the environment variables.

Requirements:
    - SECRET_KEY: A secret key for the Django project. 
        [Environment variable in: local, development, production]
    - ALLOWED_HOSTS: A list of strings representing the allowed hosts. 
        [Environment variable in: development, production]
"""

SECRET_KEY = os.environ.get('SECRET_KEY')

if SECRET_KEY == None or len(SECRET_KEY) < 30:
    running_deployment_transcript+= red_critical(f'[Critical] SECRET_KEY environment variable not set or is not sufficient in length. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True

elif "django-insecure" in SECRET_KEY:
    running_deployment_transcript+= yellow_warning(f'[Warning] SECRET_KEY is set to a default "django-insecure" value. This is not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')


# Set the debug mode.
if DEPLOYMENT == 'local':
    # SECURITY WARNING: do not run with debug turned on in production!
    DEBUG = True
    running_deployment_transcript+= yellow_warning(f'[Warning] DEBUG is set to True. This is not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
else: # development, and production
    DEBUG = False

# Set the allowed hosts.
if DEPLOYMENT == 'local':
    ALLOWED_HOSTS = ['*']
    running_deployment_transcript+= yellow_warning(f'[Warning] ALLOWED_HOSTS is set to ["*"]. This is not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
else: # development and production
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
    # Check if valid
    if len(ALLOWED_HOSTS) == 0: # if invalid
        running_deployment_transcript+= red_critical(f'[Critical] ALLOWED_HOSTS environment variable not working. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
        critical_warnings_exist = True

    if DEPLOYMENT == "production":
        if ALLOWED_HOSTS[0] == '*':
            running_deployment_transcript+= red_critical(f'[Critical] ALLOWED_HOSTS is set to ["*"]. This is highly not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
            critical_warnings_exist = True
        
        # See if localhost or 127.0.0.1 is in the allowed hosts.
        localhost_in_allowed_hosts = False
        for host in ALLOWED_HOSTS:
            if 'localhost' in host:
                if 'localhost' in host and '.' in localhost: # Fix edge case where localhost is in a valid prod url (such as localhostproduct.com)
                    pass
                else:
                    localhost_in_allowed_hosts = True
                    break
            if '127.0.0.1' in host or '0.0.0.0' in host:
                localhost_in_allowed_hosts = True
                break
        
        if localhost_in_allowed_hosts:
            running_deployment_transcript+= red_critical(f'[Critical] ALLOWED_HOSTS has localhost, 127.0.0.1, or 0.0.0.0. This is highly not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
            critical_warnings_exist = True


"""
Set the database based upon the environment variables. You
can either use a PostgreSQL database or a local Sqlite database.
If PSQL_DATABASE_URL is provided, it will be used, otherwise
LOCAL_SQLITE will be used with the default of "db.sqlite3".

Requirements:
    - PSQL_DATABASE_URL: A database URL for the project for a
PostgreSQL database with the username, password, host, port, and 
database name in the URL.
    - LOCAL_SQLITE: An alternative option if you would like to use 
a local sqlite3 database instead. This variable should be the 
name of the database, such as "db.sqlie3" or "local.sqlite3".
"""

PSQL_DATABASE_URL = os.environ.get('PSQL_DATABASE_URL')
LOCAL_SQLITE = os.environ.get('LOCAL_SQLITE')

if PSQL_DATABASE_URL==None:
    if LOCAL_SQLITE:
        running_deployment_transcript+= yellow_warning(f'[Warning] Using local database filename \"{LOCAL_SQLITE}.sqlite3\". This is ok if expected. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
        if len(LOCAL_SQLITE)<3:
            running_deployment_transcript+= red_critical(f'[Critical] LOCAL_SQLITE environment variable is likely invalid (<3 chars). (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
            critical_warnings_exist = True
        elif ".sqlite3" in LOCAL_SQLITE:
            running_deployment_transcript+= red_critical(f'[Warning] LOCAL_SQLITE environment variable is may be invalid as it contains \".sqlite3\" extension. This is not needed as the sqlite3 extension is automatically added to the name. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    else:
        running_deployment_transcript+= red_critical(f'[Warning] Both LOCAL_SQLITE and PSQL_DATABASE_URL environment variables are not set. At least one must be set to configure the database. Defaulting to \"db.sqlite3\". (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
        critical_warnings_exist = True
        LOCAL_SQLITE="db.sqlite3"
else:
    if len(PSQL_DATABASE_URL)<3:
        running_deployment_transcript+= red_critical(f'[Critical] PSQL_DATABASE_URL environment variable is likely invalid (<3 chars). (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
        critical_warnings_exist = True


"""
Set CSRF_TRUSTED_ORIGINS based upon ALLOWED_HOSTS. Can change in the future.
"""

CSRF_TRUSTED_ORIGINS =[]
if DEPLOYMENT == 'production':
    for host in ALLOWED_HOSTS:
        CSRF_TRUSTED_ORIGINS.append("https://"+host)
else:
    for host in ALLOWED_HOSTS:
        CSRF_TRUSTED_ORIGINS.append("http://"+host)
        CSRF_TRUSTED_ORIGINS.append("https://"+host)


"""
Set the database based upon the deployment environment and 
the environment variables.

Requirements:
    - DATABASES: Local SQLite3 or Database url for the postgresql database.
        [Environment variable in: development, production]
"""

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if PSQL_DATABASE_URL==None:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / (LOCAL_SQLITE+".sqlite3")),
        }
    }

#Note: currently using one database. In future when add staging and/or development servers, this can be expanded to have seperate DBs.
else:
    #connect to postgresql database from environment variables
    DATABASES = {
        'default': dj_database_url.config(default=PSQL_DATABASE_URL)
    }  


"""
Set social login with Google using previous
environment variables.
"""

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_SECRET_KEY,
        }
    }
}


# ------------- [Other Application Settings] -------------

# Application definition

INSTALLED_APPS = [
    'djgoprod',
    "accounts",
    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
]

# Important for allauth
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

# Define email settings
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Define redirect and login urls
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# Secure HTTP in production
if DEPLOYMENT != 'local' and DEPLOYMENT != 'development':
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# Use Custom User Model
AUTH_USER_MODEL = "accounts.CustomUser"

# Using session-based auth instead of JWT or other token-based auth. This can be reconfigured. It is an opinionated design choice that Django makes easy to change.
REST_AUTH = {
    'TOKEN_MODEL': None,
    'SESSION_LOGIN': True,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication', # Using session-based auth instead of JWT.
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djgoprod.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djgoprod.wsgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ------------- [Print Results] -------------

# Print divider
print("--------------------------")

# Print the deployment transcript.
print(running_deployment_transcript)

# Print the results of the settings.py deployment.
if critical_warnings_exist:
    print(red_critical(f'Critical warnings exist. Please fix before deploying. ({DEPLOYMENT} deployment)'))
else:
    print(green_success(f'No errors found in settings.py {DEPLOYMENT} deployment.'))
print("\n")

DEPLOYMENT_TRANSCRIPT = running_deployment_transcript
CRIT_WARNINGS_EXIST = critical_warnings_exist