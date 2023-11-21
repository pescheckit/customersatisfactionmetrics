from django import forms

from customersatisfactionmetrics.models import Survey


class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        survey_id = kwargs.pop('survey_id', None)
        slug = kwargs.pop('slug', None)
        super(SurveyForm, self).__init__(*args, **kwargs)

        # Fetch the survey by ID or slug
        if survey_id is not None:
            survey = Survey.objects.get(pk=survey_id)
        elif slug is not None:
            survey = Survey.objects.get(slug=slug)
        else:
            raise ValueError("Either survey_id or slug must be provided")

        for question in survey.questions.order_by('order').all():
            field_name = f'question_{question.id}'

            if survey.survey_type == 'NPS':
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text, choices=[(i, str(i)) for i in range(0, 11)]
                )
            elif survey.survey_type in ['CSAT', 'CES']:
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text, choices=[(i, str(i)) for i in range(1, 6)]
                )
            elif survey.survey_type == 'GENERIC':
                if question.response_type == 'INT':
                    # Use the int_min and int_max to set the range for the integer field
                    self.fields[field_name] = forms.IntegerField(
                        label=question.text,
                        min_value=question.int_min,
                        max_value=question.int_max
                    )
                elif question.response_type == 'TEXT':
                    self.fields[field_name] = forms.CharField(
                        label=question.text,
                        widget=forms.Textarea  # Use a textarea widget for text responses
                    )
                elif question.response_type == 'BOOL':
                    self.fields[field_name] = forms.BooleanField(label=question.text, required=False)
