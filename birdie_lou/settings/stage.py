from .base import *


SECRET_KEY = '44=w$0r2s@_14$9#mat(vgc)24c0b@uojf3j%hn4nk!pp^p&=*'
DEBUG = False
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
  }
}