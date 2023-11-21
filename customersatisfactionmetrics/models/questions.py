from django.db import models

from .surveys import Survey


class Question(models.Model):
    RESPONSE_TYPES = (
        ('INT', 'Integer'),
        ('TEXT', 'Text'),
        ('BOOL', 'Boolean'),
    )
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    response_type = models.CharField(max_length=5, choices=RESPONSE_TYPES)
    int_min = models.IntegerField(null=True, blank=True)  # Minimum value for INT response type
    int_max = models.IntegerField(null=True, blank=True)  # Maximum value for INT response type
    # Add an order field
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']  # This ensures questions are ordered by this field by default

    def save(self, *args, **kwargs):
        if self.survey.survey_type in ['CSAT', 'NPS', 'CES']:
            self.response_type = 'INT'
            # Set default ranges for specific survey types if needed
            if self.survey.survey_type == 'NPS':
                self.int_min, self.int_max = 0, 10
            elif self.survey.survey_type in ['CSAT', 'CES']:
                self.int_min, self.int_max = 1, 5
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.text