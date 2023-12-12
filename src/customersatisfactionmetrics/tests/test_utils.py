"""
This module contains tests for utility functions and custom template tags
in the Customer Satisfaction Metrics application.

It includes tests for the correct functioning of custom template tags used
to insert surveys into templates by ID or slug.
"""
import logging

from django.template import Context, Template
from django.test import TestCase

from customersatisfactionmetrics.models import Survey

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TemplateTagsTests(TestCase):
    """
    Test suite for custom template tags in the Customer Satisfaction Metrics application.

    This class tests the functionality and rendering of template tags used
    to insert survey forms into templates.
    """
    def setUp(self):
        """
        Set up function to create a survey instance for testing the template tags.
        """
        self.survey = Survey.objects.create(title="Customer Feedback", survey_type="CSAT", slug="customer-feedback")
        logger.info("TemplateTagsTests setUp completed.")

    def test_insert_survey_by_id_tag(self):
        """
        Test the 'insert_survey_by_id' template tag.
        Ensures that the survey form is correctly rendered when using the survey ID.
        """
        t = Template('{% load survey_tags %}{% insert_survey_by_id survey.id %}')
        rendered = t.render(Context({'survey': self.survey}))
        self.assertIn("Customer Feedback", rendered)  # Check for a unique part of the survey form
        logger.info("Template tag insert_survey_by_id rendered correctly.")

    def test_insert_survey_by_slug_tag(self):
        """
        Test the 'insert_survey_by_slug' template tag.
        Ensures that the survey form is correctly rendered when using the survey slug.
        """
        t = Template('{% load survey_tags %}{% insert_survey_by_slug survey.slug %}')
        rendered = t.render(Context({'survey': self.survey}))
        self.assertIn("Customer Feedback", rendered)  # Check for a unique part of the survey form
        logger.info("Template tag insert_survey_by_slug rendered correctly.")
