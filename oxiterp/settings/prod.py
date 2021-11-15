from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = True
ALLOWED_HOSTS = ['*']

# DATABASES = {
#   'default': {
#      'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'oxiterp',
#    'USER': 'oxitowner',
#   'PASSWORD': 'oxit2016',
#  'HOST': 'localhost',
# 'PORT': '5432',
# }
# }

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.mysql',
   #     'NAME': 'admin_sbs',
    #    'HOST': 'localhost',
     #   'PORT': '3306',
      #  'USER': 'admin_sbs',
       # 'PASSWORD': 'kobil2013'
    #}
#}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'sp000dbo-scan/kdstdw',
        'USER': 'yekabis',
        'PASSWORD': 'Yebis1759Ka',        
    }
}


STATIC_ROOT = "/home/yekadmin/YEKAB-S/oxiterp/static/"

STAICFILES_DIR = [

    "/home/yekadmin/YEKAB-S/oxiterp/static/"

]

try:
    from oxiterp.settings.local import *
except:
    pass
