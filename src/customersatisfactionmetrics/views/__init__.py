"""
View module for the Customer Satisfaction Metrics application.

This module imports and consolidates the views used in the application, such as
'survey_view' and 'thank_you_view', facilitating their accessibility from other modules.
"""

from .survey_view import survey_view  # noqa: F401
from .thank_you_view import thank_you_view  # noqa: F401
