from django.db import models
from django.utils.text import slugify


class Survey(models.Model):
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Survey, self).save(*args, **kwargs)

    def __str__(self):
        return self.title