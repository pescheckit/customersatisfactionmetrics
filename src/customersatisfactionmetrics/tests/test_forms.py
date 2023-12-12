import logging
from django.test import TestCase
from customersatisfactionmetrics.forms.survey_form import SurveyForm
from customersatisfactionmetrics.models import Survey, Question

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SurveyFormTest(TestCase):
    def setUp(self):
        # Create a sample survey and questions for testing
        self.survey = Survey.objects.create(title="Customer Feedback", survey_type="CSAT")
        Question.objects.create(
            survey=self.survey,
            text="How do you rate our service?",
            response_type="INT",
            int_min=1,
            int_max=5,
            order=1,
            is_required=True
        )
        logger.info("SetUp complete: Survey and question created.")

    def test_valid_data(self):
        form_data = {'question_1': 4}
        form = SurveyForm(data=form_data, survey_id=self.survey.id)
        self.assertTrue(form.is_valid())
        logger.info("Valid data test passed.")

    def test_invalid_data(self):
        # Test with data that is outside the valid range
        form_data = {'question_1': 6}
        form = SurveyForm(data=form_data, survey_id=self.survey.id)
        self.assertFalse(form.is_valid())
        self.assertIn('question_1', form.errors)
        logger.info("Invalid data test passed. Errors: %s", form.errors)

    def test_required_field(self):
        # Test with missing required field
        form = SurveyForm(data={}, survey_id=self.survey.id)
        self.assertFalse(form.is_valid())
        self.assertIn('question_1', form.errors)
        logger.info("Required field test passed. Errors: %s", form.errors)

    def test_dynamic_field_generation(self):
        # Test if the form dynamically generates the correct fields
        form = SurveyForm(survey_id=self.survey.id)
        self.assertIn('question_1', form.fields)
        logger.info("Dynamic field generation test passed.")
