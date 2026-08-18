"""
Shared model behaviour for the Customer Satisfaction Metrics application.

This module holds the subject mixin, which lets a response or an impression
point at any object in the host application, so feedback can be traced back to
the thing it was about without this package knowing what that thing is.
"""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class SubjectMixin(models.Model):
    """
    Adds an optional generic link to whatever the feedback was about.

    Knowing who answered is rarely enough. A rating collected at the end of a
    checkout says little without the order, and one collected by an anonymous
    respondent has no user at all, so the subject is the only thing tying the
    answer to its context.

    The subject is any model instance in the host application: an order, a
    screening, a ticket. Primary keys are stored as text so integer, UUID and
    slug primary keys all work.

    Attributes:
        content_type (ForeignKey): The subject's model.
        object_id (CharField): The subject's primary key, as text.
        content_object (GenericForeignKey): The subject itself.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=255, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        """
        Meta options for the SubjectMixin.
        """
        abstract = True

    @property
    def subject(self):
        """
        The object this record is about, or None when it was not linked.
        """
        return self.content_object


def subject_fields(subject):
    """
    Turn a model instance into the field values identifying it.

    Args:
        subject: Any model instance, or None.

    Returns:
        dict: Values for content_type and object_id, blank when there is no
        subject, ready to be passed to create() or update().
    """
    if subject is None:
        return {'content_type': None, 'object_id': ''}
    return {
        'content_type': ContentType.objects.get_for_model(subject),
        'object_id': str(subject.pk),
    }


def subject_filter(subject):
    """
    Build filter keyword arguments matching records about a given subject.

    Args:
        subject: Any model instance.

    Returns:
        dict: Keyword arguments for filter(), for example
        Response.objects.filter(**subject_filter(order)).
    """
    return {
        'content_type': ContentType.objects.get_for_model(subject),
        'object_id': str(subject.pk),
    }
