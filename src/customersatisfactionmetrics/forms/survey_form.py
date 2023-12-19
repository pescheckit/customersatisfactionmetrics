"""
Module for defining forms related to Surveys in the Customer Satisfaction Metrics application.

This module contains form definitions that are used for creating and handling surveys,
including dynamically generating form fields based on the survey type and question response type.
"""
from django import forms
from django.conf import settings
from customersatisfactionmetrics.models import Response, Survey


def create_generic_choice_field(question):
    """
    Create a choice field for a GENERIC survey with min and max labels.
    """
    range_choices = [(i, str(i)) for i in range(question.int_min, question.int_max + 1)]
    if question.min_label and question.max_label:
        range_choices = [(question.int_min, question.min_label)] + \
            range_choices[1:-1] + \
            [(question.int_max, question.max_label)]
    return forms.ChoiceField(
        label=question.text,
        choices=range_choices,
        widget=forms.RadioSelect,
        required=question.is_required
    )


class SurveyForm(forms.ModelForm):
    """
    Form for a Survey.

    This form dynamically generates fields based on the survey type and question
    response types. It supports different types of surveys such as NPS, CSAT, CES, and GENERIC.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize SurveyForm.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments, including 'survey_id', 'slug', and 'session_id'.
        """
        self.survey_id = kwargs.pop('survey_id', None)
        self.slug = kwargs.pop('slug', None)
        self.session_id = kwargs.pop('session_id', None)
        self.survey = None

        super().__init__(*args, **kwargs)  # Updated to Python 3 style super()

        # Fetch the survey by ID or slug
        if self.survey_id is not None:
            self.survey = Survey.objects.get(pk=self.survey_id)  # pylint: disable=no-member
        elif self.slug is not None:
            self.survey = Survey.objects.get(slug=self.slug)  # pylint: disable=no-member
        else:
            raise ValueError("Either survey_id or slug must be provided")

        self.construct_survey_fields()

    def construct_survey_fields(self):
        """
        Construct survey fields based on the survey type and question response types.
        """
        for question in self.survey.questions.order_by('order').all():
            field_name = f'question_{question.id}'
            field_required = question.is_required

            if self.survey.survey_type in ['NPS', 'CSAT', 'CES']:
                self.fields[field_name] = create_generic_choice_field(question)
            elif self.survey.survey_type == 'GENERIC':
                self.handle_generic_question(question, field_name, field_required)

            response = Response.objects.filter(question=question, session_id=self.session_id).first()
            if response:
                self.fields[field_name].initial = response.text

    def handle_generic_question(self, question, field_name, field_required):
        """
        Handle the creation of fields for a GENERIC survey type.

        Args:
            question: The question object.
            field_name: The name of the field.
            field_required: Boolean indicating whether the field is required.
        """
        if question.response_type == 'INT':
            if getattr(settings, 'SURVEY_USE_INTEGER_FIELD', True):
                self.fields[field_name] = forms.IntegerField(
                    label=question.text,
                    min_value=question.int_min,
                    max_value=question.int_max,
                    required=field_required
                )
            else:
                self.fields[field_name] = create_generic_choice_field(question)
        elif question.response_type == 'TEXT':
            self.fields[field_name] = forms.CharField(
                label=question.text,
                widget=forms.Textarea,
                required=field_required
            )
        elif question.response_type == 'BOOL':
            self.fields[field_name] = forms.BooleanField(label=question.text, required=False)

    def save(self, commit=True, **kwargs):
        """
        Save method for handling survey form data.
        """
        response = Response.objects.filter(
            question=kwargs.get('question'),
            session_id=kwargs.get('session_id'),
        )

        if response.exists():
            response.update(**kwargs)
        else:
            Response.objects.create(**kwargs)

    class Meta:
        """
        Meta class for SurveyForm.
        """
        model = Survey
        fields = []
