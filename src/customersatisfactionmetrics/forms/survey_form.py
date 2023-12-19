"""
Module for defining forms related to Surveys in the Customer Satisfaction Metrics application.

This module contains form definitions that are used for creating and handling surveys,
including dynamically generating form fields based on the survey type and question response type.
"""
from django import forms
from django.conf import settings

from customersatisfactionmetrics.models import Survey, Response


class SurveyForm(forms.ModelForm):
    """
    Form for a Survey.

    This form dynamically generates fields based on the survey type and question
    response types. It supports different types of surveys such as NPS, CSAT, CES, and GENERIC.
    """

    def __init__(self, *args, **kwargs):
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

        for question in self.survey.questions.order_by('order').all():
            field_name = f'question_{question.id}'
            field_required = question.is_required

            if self.survey.survey_type == 'NPS':
                self.fields[field_name] = self.create_generic_choice_field(question)
            elif self.survey.survey_type in ['CSAT', 'CES']:
                self.fields[field_name] = self.create_generic_choice_field(question)
            elif self.survey.survey_type == 'GENERIC':
                if question.response_type == 'INT':
                    if getattr(settings, 'SURVEY_USE_INTEGER_FIELD', True):
                        self.fields[field_name] = forms.IntegerField(
                            label=question.text,
                            min_value=question.int_min,
                            max_value=question.int_max,
                            required=field_required
                        )
                    else:
                        self.fields[field_name] = self.create_generic_choice_field(question)
                elif question.response_type == 'TEXT':
                    self.fields[field_name] = forms.CharField(
                        label=question.text,
                        widget=forms.Textarea,
                        required=field_required
                    )
                elif question.response_type == 'BOOL':
                    self.fields[field_name] = forms.BooleanField(label=question.text, required=False)

            response = Response.objects.filter(question=question, session_id=self.session_id).first()
            if response:
                self.fields[field_name].initial = response.text

    def save(self, commit=True, **kwargs):
        """
        Save method for handling survey form data.

        This method handles the saving of survey form data. If a response exists for a question
        and session ID, it updates the response; otherwise, it creates a new response.

        Args:
            commit (bool): Whether to commit the changes immediately.
            **kwargs: Additional keyword arguments for saving data.
        """
        response = Response.objects.filter(
            question = kwargs.get('question'),
            session_id = kwargs.get('session_id'),
        )

        if response.exists():
            response.update(**kwargs)
        else:
            Response.objects.create(**kwargs)

    class Meta:
        """
        Meta class for SurveyForm.

        Defines metadata for the SurveyForm class, including the model and fields.
        """
        model = Survey
        fields = []

    def create_generic_choice_field(self, question):
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
