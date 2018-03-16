"""
WSGI config for ERP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

"""
append content dirname
"""

import sys

content_dir = os.path.dirname((os.path.dirname(__file__)))

sys.path.append(content_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ERP.settings")

application = get_wsgi_application()
