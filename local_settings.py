__author__ = 'tmiller'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'loka', # Or path to database file if using sqlite3.
        'USER': 'jango', # Not used with sqlite3.
        'PASSWORD': 'jango11', # Not used with sqlite3.
        'HOST': 'vader', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306', # Set to empty string for default. Not used with sqlite3.
    }
}