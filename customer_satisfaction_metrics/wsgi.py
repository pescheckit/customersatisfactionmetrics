"""
WSGI config for customer_satisfaction_metrics project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

# Add this line before other imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customer_satisfaction_metrics.settings')

application = get_wsgi_application()
