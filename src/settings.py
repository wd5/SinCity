# -*- coding: utf-8 -*-
# Django settings for perspectiva project.
import os, platform, sys

APPEND_SLASH = False
DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (('Glader', 'glader.ru@gmail.com'),)
MANAGERS = (('Senny', 'senni@mail.ru'),)
SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'glader.ru@gmail.com'

LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/'

AUTH_PROFILE_MODULE = 'core.Profile'

PROJECT_PATH = os.path.dirname(__file__)
data_images_path = os.path.join(PROJECT_PATH, 'media/data/')
FORCE_SCRIPT_NAME = ""

TMP_FILE = '/tmp/sincity'

FOOD_DAYS = (
    (u'Четверг вечер', 180),
    (u'Пятница утро', 120),
    (u'Пятница день', 220),
    (u'Пятница вечер', 180),
    (u'Суббота утро', 120),
    (u'Суббота день', 220),
    (u'Суббота вечер', 180),
    (u'Воскресенье утро', 120),
    )

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Yekaterinburg'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1
DOMAIN = 'sincity2012.ru'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_PATH + '/media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '12345'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'core.context.default',
    'messages.context_processors.inbox',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'south',
    'core',
    'gallery',
    'newspaper',
    'messages',
    'pytils',
)

#
# Настройки сайта
#

LOG_PATH = '/var/log/projects/sincity'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-15s %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_PATH, 'traceback.log'),
            'formatter': 'verbose',
            },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'WARNING',
            'propagate': True,
            },
        }
}

try:
    from local_settings import *
except ImportError:
    pass

EXCEPTION_LOG_FILE = os.path.join(LOG_PATH, 'exception.log')
TRACEBACK_LOG_FILE = os.path.join(LOG_PATH, 'traceback.log')

LOGGING_FORMAT = '%(asctime)s %(name)-15s %(levelname)s %(message)s'
LOGGING_MAX_FILE_SIZE = 1 * 1024 * 1024 #: Максимальный размер файла с логами в байтах.
LOGGING_MAX_FILES_COUNT = 10 #: Количество бекапов файлов с логами.

WARNING_LOG_PATH = os.path.join(LOG_PATH, 'warning.log')
ADMIN_LOG_PATH = os.path.join(LOG_PATH, 'admin.log')

LOG_PDF = os.path.join(LOG_PATH,'pdf.log')
LOG_SENDMAIL = os.path.join(LOG_PATH, 'email.log')


THUMBNAIL_ROOT = os.path.join(MEDIA_ROOT, 'data/thumbnails')
THUMBNAIL_URL = 'data/thumbnails/'
THUMBNAIL_SIZE = 500, 200
