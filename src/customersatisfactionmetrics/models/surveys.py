"""
This module defines the Survey model for the Customer Satisfaction Metrics application.

It includes the Survey class which represents different types of surveys, such as CSAT,
NPS, CES, and GENERIC surveys, and contains fields like title, slug, survey type, and
creation date.
"""

from django.db import models
from django.utils.text import slugify


class Survey(models.Model):
    """
    Represents a survey in the Customer Satisfaction Metrics application.

    Attributes:
        title (CharField): The title of the survey.
        slug (SlugField): A URL-friendly slug derived from the title.
        survey_type (CharField): The type of survey (CSAT, NPS, CES, GENERIC).
        created_at (DateTimeField): The date and time when the survey was created.
    """

    SURVEY_TYPES = (
        ('CSAT', 'Customer Satisfaction'),
        ('NPS', 'Net Promoter Score'),
        ('CES', 'Customer Effort Score'),
        ('GENERIC', 'Generic Survey')
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    survey_type = models.CharField(max_length=200, choices=SURVEY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Updated to Python 3 style super()

    def __str__(self):
        return str(self.title)  # Ensure that the returned value is a string
