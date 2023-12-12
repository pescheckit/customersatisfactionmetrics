from django.test import TestCase
from customersatisfactionmetrics.models import Survey, Question
import logging

logger = logging.getLogger(__name__)

class SurveyModelTest(TestCase):
    def setUp(self):
        self.survey = Survey.objects.create(title="Customer Feedback", survey_type="CSAT")
        logger.info("SurveyModelTest setup complete. Survey created with title: %s", self.survey.title)

    def test_survey_creation(self):
        logger.info("Testing survey creation.")
        self.assertEqual(self.survey.title, "Customer Feedback")
        self.assertEqual(self.survey.survey_type, "CSAT")
        logger.info("Survey creation test passed.")

class QuestionModelTest(TestCase):
    def setUp(self):
        self.survey = Survey.objects.create(title="Customer Feedback", survey_type="CSAT")
        self.question = Question.objects.create(survey=self.survey, text="How satisfied are you?", response_type="INT")
        logger.info("QuestionModelTest setup complete. Question created with text: %s", self.question.text)

    def test_question_creation(self):
        logger.info("Testing question creation.")
        self.assertEqual(self.question.survey, self.survey)
        self.assertEqual(self.question.text, "How satisfied are you?")
        self.assertEqual(self.question.response_type, "INT")
        logger.info("Question creation test passed.")
