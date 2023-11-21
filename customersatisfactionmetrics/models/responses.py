from django.conf import settings
from django.db import models

from .questions import Question


class Response(models.Model):
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

    def __str__(self):
        return self.text
