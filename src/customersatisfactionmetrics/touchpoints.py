"""
Eligibility and bookkeeping for survey touchpoints.

The host application asks "may I show this touchpoint to this request", and this
module answers using the cooldown rules configured on the Touchpoint. Nothing in
here knows anything about the host application's own models: any grouping (an
organisation, a team, a tenant) is expressed as an opaque scope key string that
the host supplies directly or through the SURVEY_SCOPE_RESOLVER setting.
"""

import datetime
import logging

from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.utils.module_loading import import_string

from customersatisfactionmetrics.models import Impression, Touchpoint, subject_fields

logger = logging.getLogger(__name__)


def get_open_impression_ttl_hours():
    """
    Return how long an unanswered impression stays reusable, in hours.

    Within this window the same card is shown again on a page reload instead of
    silently vanishing, and no second impression is recorded. After it, the
    impression counts as ignored and the cooldown applies.
    """
    return getattr(settings, 'SURVEY_OPEN_IMPRESSION_TTL_HOURS', 24)


def resolve_scope_key(request):
    """
    Resolve the scope key for a request via the SURVEY_SCOPE_RESOLVER setting.

    The setting holds a dotted path to a callable taking the request and
    returning a string, for example "myapp.utils.current_organisation_key".
    Returns an empty string when no resolver is configured.

    Args:
        request: The HttpRequest object.

    Returns:
        str: The scope key, or an empty string.
    """
    path = getattr(settings, 'SURVEY_SCOPE_RESOLVER', None)
    if not path:
        return ''
    try:
        return import_string(path)(request) or ''
    except Exception:  # pylint: disable=broad-except
        logger.exception('SURVEY_SCOPE_RESOLVER %s failed', path)
        return ''


def get_respondent(request):
    """
    Return the (user, session_id) pair identifying the respondent.

    Args:
        request: The HttpRequest object.

    Returns:
        tuple: (user or None, session_id string which may be empty).
    """
    user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
    session_id = ''
    if getattr(request, 'session', None) is not None:
        session_id = request.session.session_key or ''
    return user, session_id


def _respondent_q(user, session_id):
    """
    Build a filter matching impressions belonging to this respondent.

    Args:
        user: The authenticated user or None.
        session_id (str): The session key, possibly empty.

    Returns:
        Q: A filter, or None when the respondent cannot be identified at all.
    """
    if user is not None:
        return Q(user=user)
    if session_id:
        return Q(session_id=session_id)
    return None


def _cooldown_queryset(touchpoint):
    """
    Return the impressions the cooldown for this touchpoint should consider.

    Args:
        touchpoint (Touchpoint): The touchpoint being evaluated.

    Returns:
        QuerySet: Impressions across all touchpoints or just this one.
    """
    if touchpoint.cooldown_scope == Touchpoint.COOLDOWN_SCOPE_TOUCHPOINT:
        return Impression.objects.filter(touchpoint=touchpoint)
    return Impression.objects.all()


def get_open_impression(touchpoint, user, session_id):
    """
    Return this respondent's still open impression for the touchpoint, if any.

    Args:
        touchpoint (Touchpoint): The touchpoint being evaluated.
        user: The authenticated user or None.
        session_id (str): The session key, possibly empty.

    Returns:
        Impression or None.
    """
    respondent = _respondent_q(user, session_id)
    if respondent is None:
        return None
    cutoff = timezone.now() - datetime.timedelta(hours=get_open_impression_ttl_hours())
    return Impression.objects.filter(
        respondent,
        touchpoint=touchpoint,
        dismissed_at__isnull=True,
        responded_at__isnull=True,
        shown_at__gte=cutoff,
    ).first()


def is_eligible(touchpoint, request, scope_key=None):
    """
    Decide whether this touchpoint may be shown for this request.

    A respondent already holding an open impression stays eligible, so that the
    card survives a page reload. Otherwise the respondent cooldown and then the
    scope cooldown are applied.

    Args:
        touchpoint (Touchpoint): The touchpoint being evaluated.
        request: The HttpRequest object.
        scope_key (str, optional): Overrides the resolved scope key.

    Returns:
        bool: True when the touchpoint may be rendered.
    """
    if not touchpoint.is_active:
        return False

    user, session_id = get_respondent(request)
    respondent = _respondent_q(user, session_id)
    if respondent is None:
        return False

    if get_open_impression(touchpoint, user, session_id) is not None:
        return True

    now = timezone.now()

    if touchpoint.cooldown_days:
        cutoff = now - datetime.timedelta(days=touchpoint.cooldown_days)
        if _cooldown_queryset(touchpoint).filter(respondent, shown_at__gte=cutoff).exists():
            return False

    if scope_key is None:
        scope_key = resolve_scope_key(request)

    if touchpoint.scope_cooldown_days and scope_key:
        cutoff = now - datetime.timedelta(days=touchpoint.scope_cooldown_days)
        if _cooldown_queryset(touchpoint).filter(scope_key=scope_key, shown_at__gte=cutoff).exists():
            return False

    return True


def record_impression(touchpoint, request, scope_key=None, subject=None):
    """
    Record that the touchpoint was shown, reusing an open impression if present.

    Args:
        touchpoint (Touchpoint): The touchpoint being shown.
        request: The HttpRequest object.
        scope_key (str, optional): Overrides the resolved scope key.
        subject (Model, optional): What the survey is being shown about, stored
            on the impression and later inherited by the responses.

    Returns:
        Impression or None when the respondent cannot be identified.
    """
    user, session_id = get_respondent(request)
    if user is None and not session_id:
        return None

    existing = get_open_impression(touchpoint, user, session_id)
    if existing is not None:
        return existing

    if scope_key is None:
        scope_key = resolve_scope_key(request)

    return Impression.objects.create(
        touchpoint=touchpoint,
        user=user,
        session_id=session_id,
        scope_key=scope_key,
        **subject_fields(subject),
    )


def _close_impression(touchpoint, request, field):
    """
    Stamp the given field on this respondent's most recent open impression.

    Args:
        touchpoint (Touchpoint): The touchpoint being closed.
        request: The HttpRequest object.
        field (str): Either "dismissed_at" or "responded_at".

    Returns:
        Impression or None when there was nothing open to close.
    """
    user, session_id = get_respondent(request)
    impression = get_open_impression(touchpoint, user, session_id)
    if impression is None:
        return None
    setattr(impression, field, timezone.now())
    impression.save(update_fields=[field])
    return impression


def mark_dismissed(touchpoint, request):
    """
    Record that the respondent dismissed the touchpoint without answering.
    """
    return _close_impression(touchpoint, request, 'dismissed_at')


def mark_responded(touchpoint, request):
    """
    Record that the respondent answered the touchpoint.
    """
    return _close_impression(touchpoint, request, 'responded_at')
