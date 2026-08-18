"""
This module defines the Touchpoint and Impression models.

A Touchpoint is a named moment in a host application where a survey may be
offered, for example right after a user finished a task. An Impression records
that a touchpoint was actually shown to somebody, and what they did with it.

Recording impressions (not just responses) is what makes it possible to enforce
a cooldown, to avoid asking the same person repeatedly, and to compute a real
response rate.
"""

from django.conf import settings
from django.db import models

from .mixins import SubjectMixin
from .surveys import Survey


class Touchpoint(models.Model):
    """
    A place in the host application where a survey can be offered.

    Attributes:
        slug (SlugField): Stable identifier used by the host application.
        title (CharField): Human readable name, shown in the admin.
        description (TextField): Optional note about when this fires.
        survey (ForeignKey): The survey to render at this touchpoint.
        is_active (BooleanField): Whether the touchpoint may be shown at all.
        cooldown_days (PositiveIntegerField): How long a respondent is left
            alone after being shown a survey.
        cooldown_scope (CharField): Whether the cooldown applies across every
            touchpoint (GLOBAL) or only to this one (TOUCHPOINT).
        scope_cooldown_days (PositiveIntegerField): Optional extra cooldown
            applied to a shared scope key, for example an organisation, so that
            a whole team is not surveyed in the same week. Zero disables it.
    """

    COOLDOWN_SCOPE_GLOBAL = 'GLOBAL'
    COOLDOWN_SCOPE_TOUCHPOINT = 'TOUCHPOINT'
    COOLDOWN_SCOPES = (
        (COOLDOWN_SCOPE_GLOBAL, 'Across all touchpoints'),
        (COOLDOWN_SCOPE_TOUCHPOINT, 'This touchpoint only'),
    )

    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    survey = models.ForeignKey(Survey, related_name='touchpoints', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    cooldown_days = models.PositiveIntegerField(default=84)
    cooldown_scope = models.CharField(max_length=20, choices=COOLDOWN_SCOPES, default=COOLDOWN_SCOPE_GLOBAL)
    scope_cooldown_days = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for the Touchpoint model.
        """
        ordering = ['slug']

    def __str__(self):
        return str(self.title)


class Impression(SubjectMixin, models.Model):
    """
    Records that a touchpoint was shown to a respondent.

    An impression starts open. It is closed either by the respondent answering
    (responded_at) or dismissing it (dismissed_at). An impression that stays
    open past the configured time to live counts as ignored.

    Attributes:
        touchpoint (ForeignKey): The touchpoint that was shown.
        user (ForeignKey): The authenticated respondent, if there was one.
        session_id (CharField): Session key, used for anonymous respondents.
        scope_key (CharField): Optional shared key such as an organisation id,
            supplied by the host application, used for scope level cooldowns.
        shown_at (DateTimeField): When the touchpoint was rendered.
        dismissed_at (DateTimeField): When the respondent dismissed it.
        responded_at (DateTimeField): When the respondent answered it.
        content_object (GenericForeignKey): Optional link to whatever the survey
            was shown about, inherited by the responses on submission.
    """

    touchpoint = models.ForeignKey(Touchpoint, related_name='impressions', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=128, blank=True)
    scope_key = models.CharField(max_length=255, blank=True)
    shown_at = models.DateTimeField(auto_now_add=True)
    dismissed_at = models.DateTimeField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """
        Meta options for the Impression model.
        """
        ordering = ['-shown_at']
        indexes = [
            models.Index(fields=['user', 'shown_at']),
            models.Index(fields=['session_id', 'shown_at']),
            models.Index(fields=['scope_key', 'shown_at']),
        ]

    @property
    def is_open(self):
        """
        Whether the respondent has neither answered nor dismissed this yet.
        """
        return self.dismissed_at is None and self.responded_at is None

    def __str__(self):
        return f'{self.touchpoint} shown at {self.shown_at}'
