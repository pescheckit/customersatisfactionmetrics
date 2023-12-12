"""
This module defines the Question model for the Customer Satisfaction Metrics application.

It includes the Question class with fields and methods to represent survey questions,
along with their types, ordering, and whether they are required.
"""

from django.db import models

from .surveys import Survey


class Question(models.Model):
    """
    Represents a question in a survey.

    Attributes:
        survey (ForeignKey): The survey to which the question belongs.
        text (TextField): The text of the question.
        response_type (CharField): The type of response (e.g., INT, TEXT, BOOL).
        int_min (IntegerField): Minimum value for INT response type, optional.
        int_max (IntegerField): Maximum value for INT response type, optional.
        order (IntegerField): The display order of the question in the survey.
        is_required (BooleanField): Indicates whether the question is required.
    """

    RESPONSE_TYPES = (
        ('INT', 'Integer'),
        ('TEXT', 'Text'),
        ('BOOL', 'Boolean'),
    )
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    response_type = models.CharField(max_length=5, choices=RESPONSE_TYPES)
    int_min = models.IntegerField(null=True, blank=True)
    int_max = models.IntegerField(null=True, blank=True)
    min_label = models.CharField(max_length=255, null=True, blank=True)
    max_label = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)
    is_required = models.BooleanField(default=True)

    class Meta:
        """
        Meta options for the Question model.
        """
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.survey.survey_type in ['CSAT', 'NPS', 'CES']:
            self.response_type = 'INT'
            if self.survey.survey_type == 'NPS':
                self.int_min, self.int_max = 0, 10
            elif self.survey.survey_type in ['CSAT', 'CES']:
                self.int_min, self.int_max = 1, 5
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.text)
