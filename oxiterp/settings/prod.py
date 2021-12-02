from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = True
ALLOWED_HOSTS = ['yekabis.enerji.gov.tr']

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
        'USER': 'ekabis',
        'PASSWORD': 'qwerty1234',        
    }
}


SESSION_COOKIE_SECURE = True
STATIC_URL = '/static/'
STATIC_ROOT = '/home/yekadmin/static/'
#LDAP_URL = 'https://api.enerji.gov.tr/apigateway/merkezi-ldap-api'
LDAP_URL = 'https://servisetkb.enerji.gov.tr/etkb/servis/epassport-gateway'
LDAP_USERNAME = 'yekabis_user'
LDAP_PASSWORD = 'YeC@38c47c15!!'
LDAP_SECRET = 'deneme'


try:
    from oxiterp.settings.local import *
except:
    pass
