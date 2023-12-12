"""
This module contains tests for forms in the Customer Satisfaction Metrics application.

It includes tests for form validation, handling of valid and invalid data,
dynamic field generation based on survey types, and other form-related functionalities.
"""
import logging

from customersatisfactionmetrics.forms.survey_form import SurveyForm
from customersatisfactionmetrics.tests.base_tests import BaseSurveyTestCase

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SurveyFormTest(BaseSurveyTestCase):
    """
    Test suite for validating the SurveyForm of the Customer Satisfaction Metrics application.

    This class contains tests to ensure that the SurveyForm behaves as expected. It checks
    various aspects of the form, including the handling of valid and invalid data,
    dynamic field generation based on survey configuration, and proper form rendering.
    """
    def test_valid_data(self):
        """
        Test the form with valid data input.
        Ensures that the form is valid and all fields are correctly processed.
        """
        form_data = {'question_1': 4}
        form = SurveyForm(data=form_data, survey_id=self.survey.id)
        self.assertTrue(form.is_valid())
        logger.info("Valid data test passed.")

    def test_invalid_data(self):
        """
        Test the form with invalid data input.
        Checks that the form is invalid and appropriate errors are raised.
        """
        form_data = {'question_1': 6}
        form = SurveyForm(data=form_data, survey_id=self.survey.id)
        self.assertFalse(form.is_valid())
        self.assertIn('question_1', form.errors)
        logger.info("Invalid data test passed. Errors: %s", form.errors)

    def test_required_field(self):
        """
        Test the behavior of the form when a required field is not provided.
        Ensures that the form is invalid and the required field error is triggered.
        """
        form = SurveyForm(data={}, survey_id=self.survey.id)
        self.assertFalse(form.is_valid())
        self.assertIn('question_1', form.errors)
        logger.info("Required field test passed. Errors: %s", form.errors)

    def test_dynamic_field_generation(self):
        """
        Test the dynamic generation of form fields based on the survey type.
        Ensures that the form fields are correctly generated and populated.
        """
        form = SurveyForm(survey_id=self.survey.id)
        self.assertIn('question_1', form.fields)
        logger.info("Dynamic field generation test passed.")
