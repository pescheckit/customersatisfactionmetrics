"""
This module defines the Response model for the Customer Satisfaction Metrics application.

It contains the Response class, which represents the responses given by users to various
survey questions, including the type of response and associated user details.
"""

from django.conf import settings
from django.db import models

from .questions import Question


class Response(models.Model):
    """
    Represents a user's response to a survey question.

    Attributes:
        user (ForeignKey): The user who provided the response.
        question (ForeignKey): The question to which the response relates.
        response_type (CharField): The type of response (CSAT, NPS, CES, GENERIC).
        text (TextField): The text content of the response.
        ip_address (GenericIPAddressField): The IP address of the user at the time of response.
        user_agent (TextField): The user agent of the user's device for the response.
    """

    RESPONSE_TYPES = (
        ('CSAT', 'Customer Satisfaction'),
        ('NPS', 'Net Promoter Score'),
        ('CES', 'Customer Effort Score'),
        ('GENERIC', 'Generic Survey')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.ForeignKey(Question, related_name='responses', on_delete=models.CASCADE)
    response_type = models.CharField(max_length=22, choices=RESPONSE_TYPES)
    text = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    session_id = models.CharField(max_length=128, default='default_session_id')

    def __str__(self):
        return str(self.text)  # Ensure that the returned value is a string
