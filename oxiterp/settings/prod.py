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


LDAP_URL = 'https://api.enerji.gov.tr/apigateway/merkezi-ldap-api'
LDAP_USERNAME = 'yekabis_user'
LDAP_PASSWORD = 'YeC@38c47c15!!'
LDAP_SECRET = 'deneme'

STATIC_ROOT = "C:/Bitnami/djangostack-2.2.12-0/apache2/htdocs/static/"

STAICFILES_DIR = [

    "C:/Bitnami/djangostack-2.2.12-0/apache2/htdocs/static/"

]

try:
    from oxiterp.settings.local import *
except:
    pass
