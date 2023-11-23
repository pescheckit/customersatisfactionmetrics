"""
Django app configuration for the Customer Satisfaction Metrics app.

This module contains the AppConfig subclass for the Customer Satisfaction Metrics
application. It is used by Django for application configuration purposes.
"""

from django.apps import AppConfig


class CustomersatisfactionmetricsConfig(AppConfig):
    """
    AppConfig subclass for the Customer Satisfaction Metrics application.

    It defines the configuration settings for the application, such as the default
    auto field type and the application name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "customersatisfactionmetrics"
