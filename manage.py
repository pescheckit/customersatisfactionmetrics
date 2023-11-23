#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script allows you to perform various Django administrative tasks such as running
the development server, creating migrations, applying migrations, and running tests.
It is a thin wrapper around `django.core.management.execute_from_command_line`.
"""

import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customer_satisfaction_metrics.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
