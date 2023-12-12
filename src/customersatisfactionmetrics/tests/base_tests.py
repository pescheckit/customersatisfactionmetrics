# customersatisfactionmetrics/tests/base.py
import logging

from django.test import TestCase

from customersatisfactionmetrics.models import Question, Survey

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BaseSurveyTestCase(TestCase):
    """
    Base class for survey-related test cases in the Customer Satisfaction Metrics application.

    This class provides a common setup for tests that involve Survey and Question models.
    It creates a survey and a question instance that can be used across different test classes,
    reducing the need for repetitive code and ensuring consistency in test setup.
    """

    def setUp(self):
        """
        Set up a common test environment for Survey-related tests.

        This method initializes a survey and a question, which are commonly
        used in multiple test classes.
        """
        logger.info("Setting up base test case for survey.")
        self.survey = Survey.objects.create(title="Customer Feedback", survey_type="CSAT")
        self.question = Question.objects.create(
            survey=self.survey,
            text="How do you rate our service?",
            response_type="INT",
            int_min=1,
            int_max=5,
            order=1,
            is_required=True
        )
        logger.info("Base test case setup completed.")
