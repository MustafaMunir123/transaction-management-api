"""
ASGI config for transaction_management_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# Standard Library Imports
import os

# Third Party Imports
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transaction_management_api.settings")

application = get_asgi_application()
