#coding: utf-8

from settings_base import *


ALLOWED_HOSTS = [
    'smartfocus.local',
]


# SECURITY WARNING: don’t let this public key leak.
# Apart from the person who manages your production application
# no one should ever see this key.
# Rotate this key on regular basis.
SECRET_KEY = ')FUDEUFEHRWUEHekwalkd;adaDFfoekfAEF@E32d0*F&ERh39)(#&Y!DHec'



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


INSTALLED_APPS += [
    'django_extensions',
]



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
    }
}
