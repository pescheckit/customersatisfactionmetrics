"""
Views for submitting and dismissing surveys offered at a touchpoint.

Both views are POST only and always send the visitor back where they came from,
so a touchpoint can be embedded on any page of the host application without that
page needing to know anything about survey handling.
"""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from customersatisfactionmetrics.forms.survey_form import SurveyForm
from customersatisfactionmetrics.models import Touchpoint
from customersatisfactionmetrics.touchpoints import get_open_impression, get_respondent, mark_dismissed, mark_responded
from customersatisfactionmetrics.views.survey_view import generate_unique_session_id, process_form_submission


def _redirect_back(request):
    """
    Return a redirect to the page the touchpoint was rendered on.

    Falls back to the site root when neither the "next" parameter nor the
    referer can be trusted.

    Args:
        request: The HttpRequest object.

    Returns:
        HttpResponseRedirect: Where to send the visitor next.
    """
    target = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    if not url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        target = '/'
    return HttpResponseRedirect(target)


@require_POST
def touchpoint_submit_view(request, slug):
    """
    Store the answers given at a touchpoint and close its impression.

    An invalid form is treated the same as a valid one from the visitor's point
    of view: they are sent back to their page rather than shown form errors,
    because a touchpoint is an optional aside and must never block the task the
    visitor was actually doing.

    Args:
        request: The HttpRequest object.
        slug (str): The slug of the touchpoint being answered.

    Returns:
        HttpResponseRedirect: Back to the originating page.
    """
    touchpoint = get_object_or_404(Touchpoint, slug=slug, is_active=True)
    form = SurveyForm(
        request.POST,
        slug=touchpoint.survey.slug,
        session_id=generate_unique_session_id(request),
    )
    if form.is_valid():
        # The subject is read back off the impression rather than posted with the
        # form, so a respondent cannot relabel their answer as being about
        # somebody else's object.
        user, session_id = get_respondent(request)
        impression = get_open_impression(touchpoint, user, session_id)
        subject = impression.content_object if impression is not None else None

        process_form_submission(request, form, touchpoint.survey, subject=subject)
        mark_responded(touchpoint, request)
    return _redirect_back(request)


@require_POST
def touchpoint_dismiss_view(request, slug):
    """
    Record that the visitor dismissed a touchpoint without answering it.

    Args:
        request: The HttpRequest object.
        slug (str): The slug of the touchpoint being dismissed.

    Returns:
        HttpResponseRedirect: Back to the originating page.
    """
    touchpoint = get_object_or_404(Touchpoint, slug=slug)
    mark_dismissed(touchpoint, request)
    return _redirect_back(request)
