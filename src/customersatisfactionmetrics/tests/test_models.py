"""
This module contains tests for models in the Customer Satisfaction Metrics application.

It includes tests for the creation and validation of model instances,
such as surveys and questions, ensuring they are correctly saved and retrieved from the database.
"""
import logging

from django.test import TestCase

from customersatisfactionmetrics.models import Question, Survey

logger = logging.getLogger(__name__)


class SurveyModelTest(TestCase):
    """
    Test suite for the Survey model.

    This class tests the creation and retrieval of Survey instances,
    ensuring their fields are correctly set and saved.
    """
    def setUp(self):
        """
        Set up function to create a survey instance for the test methods.
        """
        self.survey = Survey.objects.create(title="Customer Feedback", survey_type="CSAT")
        logger.info("SurveyModelTest setup complete. Survey created with title: %s", self.survey.title)

    def test_survey_creation(self):
        """
        Test the creation of a Survey instance.
        Ensures that all attributes are correctly set and saved.
        """
        logger.info("Testing survey creation.")
        self.assertEqual(self.survey.title, "Customer Feedback")
        self.assertEqual(self.survey.survey_type, "CSAT")
        logger.info("Survey creation test passed.")


class QuestionModelTest(TestCase):
    """
    Test suite for the Question model.

    This class tests the creation and retrieval of Question instances,
    ensuring they are correctly associated with surveys and their fields are accurate.
    """
    def setUp(self):
        """
        Set up function to create a survey and associated question for the test methods.
        """
        self.survey = Survey.objects.create(title="Customer Feedback", survey_type="CSAT")
        self.question = Question.objects.create(survey=self.survey, text="How satisfied are you?", response_type="INT")
        logger.info("QuestionModelTest setup complete. Question created with text: %s", self.question.text)

    def test_question_creation(self):
        """
        Test the creation of a Question instance.
        Ensures that the question is correctly linked to a survey and all fields are accurately set.
        """
        logger.info("Testing question creation.")
        self.assertEqual(self.question.survey, self.survey)
        self.assertEqual(self.question.text, "How satisfied are you?")
        self.assertEqual(self.question.response_type, "INT")
        logger.info("Question creation test passed.")
