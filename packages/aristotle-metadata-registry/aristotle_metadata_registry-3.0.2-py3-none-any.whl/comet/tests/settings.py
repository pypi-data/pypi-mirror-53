from aristotle_mdr.tests.settings.settings import *
from aristotle_mdr.required_settings import INSTALLED_APPS

INSTALLED_APPS = (
    #The good stuff
    'comet',
    'aristotle_dse',
) + INSTALLED_APPS

ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] = ['comet']

ROOT_URLCONF = 'comet.tests.urls'
