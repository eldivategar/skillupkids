import os
from .settings import *

SECRET_KEY = 'django-insecure-shst$+ksll6x&wmyrsy69%7r%(sd(o=9g2lw61d_16xkdv*n-)'
DEBUG = False
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
        },
    }
}