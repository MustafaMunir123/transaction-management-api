"""
WSGI config for transaction_management_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

# Standard Library Imports
import os

# Third Party Imports
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transaction_management_api.settings")

application = get_wsgi_application()
