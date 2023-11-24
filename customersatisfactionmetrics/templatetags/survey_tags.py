"""
Template tags for the Customer Satisfaction Metrics application.

This module provides custom template tags for inserting survey forms into templates.
It includes tags for inserting surveys by their ID or slug.
"""

from django import template

from customersatisfactionmetrics.forms.survey_form import SurveyForm
from customersatisfactionmetrics.models import Survey

register = template.Library()


@register.inclusion_tag('survey_form.html')
def insert_survey_by_id(survey_id):
    """
    Template tag for inserting a survey form by its ID.

    Retrieves a survey by its ID and generates a corresponding SurveyForm.
    
    Args:
        survey_id (int): The ID of the survey to be retrieved and displayed.

    Returns:
        dict: A dictionary containing the survey and its form.
    """
    survey = Survey.objects.get(pk=survey_id)
    form = SurveyForm(survey_id=survey_id)
    return {'form': form, 'survey': survey}


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
    survey = Survey.objects.get(slug=slug)
    form = SurveyForm(slug=slug)
    return {'form': form, 'survey': survey}
