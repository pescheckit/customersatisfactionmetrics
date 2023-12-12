import logging
from django.test import TestCase
from django.template import Context, Template
from customersatisfactionmetrics.models import Survey

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TemplateTagsTests(TestCase):
    def setUp(self):
        # Create a sample survey for testing
        self.survey = Survey.objects.create(title="Customer Feedback", survey_type="CSAT", slug="customer-feedback")
        logger.info("TemplateTagsTests setUp completed.")

    def test_insert_survey_by_id_tag(self):
        # Render the template tag and assert the survey form is correctly included
        t = Template('{% load survey_tags %}{% insert_survey_by_id survey.id %}')
        rendered = t.render(Context({'survey': self.survey}))
        self.assertIn("Customer Feedback", rendered)  # Check for a unique part of the survey form
        logger.info("Template tag insert_survey_by_id rendered correctly.")

    def test_insert_survey_by_slug_tag(self):
        # Render the template tag and assert the survey form is correctly included
        t = Template('{% load survey_tags %}{% insert_survey_by_slug survey.slug %}')
        rendered = t.render(Context({'survey': self.survey}))
        self.assertIn("Customer Feedback", rendered)  # Check for a unique part of the survey form
        logger.info("Template tag insert_survey_by_slug rendered correctly.")
