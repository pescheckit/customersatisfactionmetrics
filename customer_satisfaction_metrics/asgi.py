"""
ASGI config for customer_satisfaction_metrics project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import sys

from django.core.asgi import get_asgi_application  # pylint: disable=import-error,no-name-in-module

# Add this line before other imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "customer_satisfaction_metrics.settings"
)

application = get_asgi_application()
