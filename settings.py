# -*- coding: utf-8 -*-
# Django settings for perspectiva project.
import os, platform, sys

APPEND_SLASH = False

ADMINS = (
    ('Glader', 'glader@glader.ru'),
)

MANAGERS = (
    ('Senny', 'senni@mail.ru'),
)

SERVER_EMAIL = 'robot@sincity2012.ru'

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DATABASE_OPTIONS = {
                    "init_command": "SET storage_engine=MYISAM",
                    'charset': 'utf8',
                    }

LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/'

AUTH_PROFILE_MODULE = 'core.Profile'

PROJECT_PATH = os.path.dirname(__file__)
data_images_path = os.path.join(PROJECT_PATH, 'media/data/')
FORCE_SCRIPT_NAME = ""

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
SECRET_KEY = '(q3s-v$9jv#x&ow)w_+*vxeag*&tt76asdbco^(Rk#z&jb!j=*bgctzhivv#efmj'

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
    'core.middleware.Process404Middleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django_errorlog',
    'django_russian',
    'south',
    'core',
    'newspaper',
    'messages',
    'django.contrib.sites',
    'django.contrib.flatpages',
)

#
# Настройки сайта
#


if platform.node() == 'u13550':
    # production
    sys.path.append('/home/www/projects/applications')

    DEBUG = False
    TEMPLATE_DEBUG = False

    DATABASE_NAME = 'sincity'             # Or path to database file if using sqlite3.
    DATABASE_USER = 'sincity'             # Not used with sqlite3.
    DATABASE_PASSWORD = ''         # Not used with sqlite3.

    DOMAIN = 'sincity2012.ru'

    # Логи
    LOG_PATH = '/var/log/projects/sincity'


else:
    # development
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    IS_DEVEL = True
    TIMING = False

    DOMAIN = 'localhost:8000'

    DATABASE_NAME = 'sincity'             # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'             # Not used with sqlite3.
    DATABASE_PASSWORD = ''         # Not used with sqlite3.

    LOG_PATH = 'log'

    INTERNAL_IPS = '127.0.0.1'

    MEDIA_URL = 'http://sincity.localhost:8088/media/'


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