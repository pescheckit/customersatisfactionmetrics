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

# Add this line to your existing settings
SURVEY_SELF_POST = True

# Dotted path to a callable taking the request and returning a string used to group
# respondents for scope level cooldowns, for example an organisation or tenant id.
# Leave as None when no grouping is needed.
SURVEY_SCOPE_RESOLVER = None

# How long an unanswered touchpoint stays reusable, in hours. Within this window a
# page reload shows the same card again instead of it vanishing, and records no
# second impression. After it, the impression counts as ignored.
SURVEY_OPEN_IMPRESSION_TTL_HOURS = 24
