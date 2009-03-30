﻿# Django settings for pollango project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Chongqing'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

#CACHE_BACKEND = "dummy:///"
#CACHE_BACKEND = "memcached:///"

#CACHE_MIDDLEWARE_SECONDS=60*2

#INTERNAL_IPS = ('127,0.0.1', )
#MIDDLEWARE_CLASSES = (

#    'django.middleware.cache.CacheMiddleware',
#    'django.middleware.common.CommonMiddleware',


#)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#a1g)i%hz+f)44a0wea9ln!g+#=#tke!0@-k)gt=&m#ec-ir=&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)



ROOT_URLCONF = 'jieblog.urls'


ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".  Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # ROOT_PATH + '/jsimple',
    ROOT_PATH + '/TextStyle',
    ROOT_PATH + '/administrator',
    ROOT_PATH + '/admin',
)

INSTALLED_APPS = (
    'jieblog.applications',
    'jieblog.wiki',
)
