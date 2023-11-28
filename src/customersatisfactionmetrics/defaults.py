"""
Default configuration settings for the Customer Satisfaction Metrics application.

This module defines default values for various configuration options used within the
Customer Satisfaction Metrics app. These settings can be overridden in the main
Django settings file of the project.
"""

# Set to False to disable the survey by ID URL, keep in mind when enabling you can enumerate the survey urls
SURVEY_ENABLE_ID_URL = False

# Set to True to use integer fields instead of other field types
SURVEY_USE_INTEGER_FIELD = False
