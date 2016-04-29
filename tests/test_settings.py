from __future__ import absolute_import

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'very-secret-string-only-used-for-testing-please-change!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
