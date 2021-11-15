"""
WSGI config for oxiterp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os, sys


sys.path.append('C:/Users/Administrator/Bitnami Django Stack projects/HalterSbs')
os.environ.setdefault("PYTHON_EGG_CACHE", "C:/Users/Administrator/Bitnami Django Stack projects/Project/egg_cache")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oxiterp.settings.prod')

application = get_wsgi_application()
