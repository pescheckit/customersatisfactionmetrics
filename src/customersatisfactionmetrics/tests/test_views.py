"""
This module contains tests for views in the Customer Satisfaction Metrics application.

It includes tests for the rendering and behavior of various views,
such as survey display and submission views, ensuring they respond with the correct templates and status codes.
"""
import logging

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from customersatisfactionmetrics.tests.base_tests import BaseSurveyTestCase

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SurveyViewTests(BaseSurveyTestCase):
    """
    Test suite for the survey-related views in the Customer Satisfaction Metrics application.

    This class tests the survey view functionality, including response to GET and POST requests,
    form rendering, and survey submission handling.
    """
    def setUp(self):
        """
        Set up function to create necessary URLs for the survey view tests.
        """
        super().setUp()  # Call setUp from BaseSurveyTestCase to set up survey and question
        self.url_slug = reverse('survey_view_by_slug', kwargs={'slug': self.survey.slug})
        if getattr(settings, 'SURVEY_ENABLE_ID_URL', False):
            self.url_id = reverse('survey_view_by_id', args=[self.survey.id])
        logger.info("SurveyViewTests setUp completed.")

    def test_survey_view_get_by_slug(self):
        """
        Test the survey view for a GET request using a slug.
        Ensures the survey form is correctly rendered and returned.
        """
        response = self.client.get(self.url_slug)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'survey_form.html')
        logger.info("Survey view GET request by slug test passed.")

    def test_survey_view_get_by_id(self):
        """
        Test the survey view for a GET request using an ID.
        Ensures the survey form is correctly rendered and returned.
        """
        if getattr(settings, 'SURVEY_ENABLE_ID_URL', False):
            response = self.client.get(self.url_id)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'survey_form.html')
            logger.info("Survey view GET request by ID test passed.")


class ThankYouViewTests(TestCase):
    """
    Test suite for the 'thank you' view in the Customer Satisfaction Metrics application.

    Contains tests to ensure that the 'thank you' page renders correctly after
    survey submission.
    """
    def setUp(self):
        """
        Set up the test environment for ThankYouViewTests.

        This method initializes the test environment before each test method is run.
        It sets up a URL for testing the 'thank you' view.
        """
        self.url = reverse('thank_you')
        logger.info("ThankYouViewTests setUp completed.")

    def test_thank_you_view(self):
        """
        Test the 'thank you' view for correct HTTP response and template usage.

        This test ensures that the 'thank you' view responds with a status code of 200
        and uses the correct template when accessed via a GET request.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thank_you.html')
        logger.info("Thank you view test passed.")
