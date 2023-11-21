from django import template

from customersatisfactionmetrics.forms.survey_form import SurveyForm
from customersatisfactionmetrics.models import Survey

register = template.Library()

@register.inclusion_tag('survey_form.html')
def insert_survey_by_id(survey_id):
    survey = Survey.objects.get(pk=survey_id)
    form = SurveyForm(survey_id=survey_id)
    return {'form': form, 'survey': survey}

@register.inclusion_tag('survey_form.html')
def insert_survey_by_slug(slug):
    survey = Survey.objects.get(slug=slug)
    form = SurveyForm(slug=slug)
    return {'form': form, 'survey': survey}
