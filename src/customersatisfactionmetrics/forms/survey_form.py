"""
Module for defining forms related to Surveys in the Customer Satisfaction Metrics application.

This module contains form definitions that are used for creating and handling surveys,
including dynamically generating form fields based on the survey type and question response type.
"""

from django import forms
from django.conf import settings

from customersatisfactionmetrics.models import Survey


class SurveyForm(forms.Form):
    """
    Form for a Survey.

    This form dynamically generates fields based on the survey type and question
    response types. It supports different types of surveys such as NPS, CSAT, CES, and GENERIC.
    """

    def __init__(self, *args, **kwargs):
        survey_id = kwargs.pop('survey_id', None)
        slug = kwargs.pop('slug', None)
        super().__init__(*args, **kwargs)  # Updated to Python 3 style super()

        # Fetch the survey by ID or slug
        if survey_id is not None:
            survey = Survey.objects.get(pk=survey_id)  # pylint: disable=no-member
        elif slug is not None:
            survey = Survey.objects.get(slug=slug)  # pylint: disable=no-member
        else:
            raise ValueError("Either survey_id or slug must be provided")

        for question in survey.questions.order_by('order').all():
            field_name = f'question_{question.id}'
            field_required = question.is_required

            if survey.survey_type == 'NPS':
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text, choices=[(i, str(i)) for i in range(0, 11)],
                    required=field_required,
                )
            elif survey.survey_type in ['CSAT', 'CES']:
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text, choices=[(i, str(i)) for i in range(1, 6)],
                    required=field_required,
                )
            elif survey.survey_type == 'GENERIC':
                if question.response_type == 'INT':
                    if getattr(settings, 'SURVEY_USE_INTEGER_FIELD', True):
                        self.fields[field_name] = forms.IntegerField(
                            label=question.text,
                            min_value=question.int_min,
                            max_value=question.int_max,
                            required=field_required
                        )
                    else:
                        # Define a range based on int_min and int_max
                        range_choices = [(i, str(i)) for i in range(question.int_min, question.int_max + 1)]
                        self.fields[field_name] = forms.ChoiceField(
                            label=question.text,
                            choices=range_choices,
                            widget=forms.RadioSelect,
                            required=field_required
                        )
                elif question.response_type == 'TEXT':
                    self.fields[field_name] = forms.CharField(
                        label=question.text,
                        widget=forms.Textarea,
                        required=field_required
                    )
                elif question.response_type == 'BOOL':
                    self.fields[field_name] = forms.BooleanField(label=question.text, required=False)
