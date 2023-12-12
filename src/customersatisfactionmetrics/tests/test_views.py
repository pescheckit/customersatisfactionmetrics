# src/customersatisfactionmetrics/tests/test_views.py
import logging
from django.test import TestCase
from django.urls import reverse
from customersatisfactionmetrics.models import Survey, Question
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SurveyViewTests(TestCase):
    def setUp(self):
        # Create a sample survey and question for testing
        self.survey = Survey.objects.create(title="Customer Feedback", survey_type="CSAT", slug="customer-feedback")
        self.question = Question.objects.create(
            survey=self.survey,
            text="How do you rate our service?",
            response_type="INT",
            int_min=1,
            int_max=5,
            order=1,
            is_required=True
        )
        self.url_slug = reverse('survey_view_by_slug', kwargs={'slug': self.survey.slug})
        if getattr(settings, 'SURVEY_ENABLE_ID_URL', False):
            self.url_id = reverse('survey_view_by_id', args=[self.survey.id])
        logger.info("SurveyViewTests setUp completed.")

    def test_survey_view_get_by_slug(self):
        response = self.client.get(self.url_slug)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'survey_form.html')
        logger.info("Survey view GET request by slug test passed.")

    def test_survey_view_get_by_id(self):
        if getattr(settings, 'SURVEY_ENABLE_ID_URL', False):
            response = self.client.get(self.url_id)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'survey_form.html')
            logger.info("Survey view GET request by ID test passed.")

class ThankYouViewTests(TestCase):
    def setUp(self):
        self.url = reverse('thank_you')
        logger.info("ThankYouViewTests setUp completed.")

    def test_thank_you_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thank_you.html')
        logger.info("Thank you view test passed.")
