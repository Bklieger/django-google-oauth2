"""
global_utils.py file for djgoprod app. Global util 
functions for the djgoprod project.

Author(s): Benjamin Klieger
Date: 2024-06-01
"""

#------- [Functions] -------#

# Function to format message to green with prefix newline.
def green_success(message: str) -> str:
    return f'\n\033[92m {message} \033[0m'

# Function to format message to yellow with prefix newline.
def yellow_warning(message: str) -> str:
    return f'\n\033[93m {message} \033[0m'

# Function to format message to red with prefix newline.
def red_critical(message: str) -> str:
    return f'\n\033[91m {message} \033[0m'
