"""
Template tags for the Customer Satisfaction Metrics application.

This module provides custom template tags for inserting survey forms into templates.
It includes tags for inserting surveys by their ID or slug, and a tag for rendering
a touchpoint, which only renders when the visitor is currently eligible for it.
"""

from django import template

from customersatisfactionmetrics.forms.survey_form import SurveyForm
from customersatisfactionmetrics.models import Survey, Touchpoint
from customersatisfactionmetrics.touchpoints import is_eligible, record_impression

register = template.Library()

FIELD_KINDS = {
    'INT': 'scale',
    'TEXT': 'text',
    'BOOL': 'bool',
}


@register.inclusion_tag('survey_form.html')
def insert_survey_by_id(survey_id):
    """
    Template tag for inserting a survey form by its ID.

    Retrieves a survey by its ID and generates a corresponding SurveyForm.
    Includes error handling for cases where
    a survey with the given ID does not exist.

    Args:
        survey_id (int): The ID of the survey to be retrieved and displayed.

    Returns:
        dict: A dictionary containing the survey and its form.
        Returns None for both survey and form if survey is not found.
    """
    try:
        survey = Survey.objects.get(pk=survey_id)
        form = SurveyForm(survey_id=survey_id)
        return {'form': form, 'survey': survey}
    except Survey.DoesNotExist:
        # Handle the case where the survey does not exist
        return {'form': None, 'survey': None}


@register.inclusion_tag('survey_form.html')
def insert_survey_by_slug(slug):
    """
    Template tag for inserting a survey form by its slug.

    Retrieves a survey by its slug and generates a corresponding SurveyForm.

    Args:
        slug (str): The slug of the survey to be retrieved and displayed.

    Returns:
        dict: A dictionary containing the survey and its form.
    """
    try:
        survey = Survey.objects.get(slug=slug)
        form = SurveyForm(slug=slug)
        return {'form': form, 'survey': survey}
    except Survey.DoesNotExist:
        return {'form': None, 'survey': None}


def _describe_fields(form):
    """
    Pair every bound field with the kind of widget the card should draw.

    Args:
        form (SurveyForm): The form whose fields should be described.

    Returns:
        list: Dictionaries holding the bound field and its kind.
    """
    described = []
    for question in form.questions:
        field = form[f'question_{question.id}']
        described.append({
            'field': field,
            'kind': FIELD_KINDS.get(question.response_type, 'text'),
            'question': question,
        })
    return described


@register.inclusion_tag('touchpoint_card.html', takes_context=True)
def survey_touchpoint(context, slug, scope_key=None, subject=None):
    """
    Render the survey attached to a touchpoint, but only when it is due.

    Renders nothing at all when the touchpoint does not exist, is inactive, or
    the visitor is inside a cooldown, so it is safe to leave this tag in a
    shared template. Showing the card records an impression, which is what the
    cooldown is later measured against.

    Requires the request context processor, since eligibility depends on the
    current visitor.

    Args:
        context: The template context.
        slug (str): The slug of the touchpoint to render.
        scope_key (str, optional): Overrides the resolved scope key.
        subject (Model, optional): What the survey is about, for example the
            order just placed. It is stored on the impression and inherited by
            the answers, so feedback stays traceable even from a visitor who is
            not signed in.

    Returns:
        dict: The context for the card template.
    """
    empty = {'touchpoint': None}
    request = context.get('request')
    if request is None:
        return empty

    touchpoint = Touchpoint.objects.filter(slug=slug).select_related('survey').first()
    if touchpoint is None or not is_eligible(touchpoint, request, scope_key=scope_key):
        return empty

    form = SurveyForm(slug=touchpoint.survey.slug)
    record_impression(touchpoint, request, scope_key=scope_key, subject=subject)

    return {
        'touchpoint': touchpoint,
        'survey': touchpoint.survey,
        'form': form,
        'fields': _describe_fields(form),
        'next': request.get_full_path(),
        'csrf_token': context.get('csrf_token'),
    }
