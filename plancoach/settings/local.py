from .base import *

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = env('SECRET_KEY')
PORTONE_SHOP_ID= env('PORTONE_SHOP_ID')
PORTONE_API_KEY= env('PORTONE_API_KEY')
PORTONE_API_SECRET= env('PORTONE_API_SECRET')
SENS_SERVICE_KEY= env('SENS_SERVICE_KEY')
SENS_SECRET_KEY= env('SENS_SECRET_KEY')
SENS_ACCESS_KEY= env('SENS_ACCESS_KEY')
DEBUG = True

ALLOWED_HOSTS = ['*'] #모든 호스트를 허용

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}