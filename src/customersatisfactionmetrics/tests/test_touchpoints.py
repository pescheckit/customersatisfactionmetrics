"""
Tests for touchpoint eligibility, impressions and the rendering template tag.

These cover the rules that decide whether a survey is shown: the respondent
cooldown, the scope cooldown, reuse of an open impression across a page reload,
and the recording of dismissals so that ignoring a card is distinguishable from
never having seen one.
"""

import datetime
import logging

from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import RequestFactory, TestCase
from django.utils import timezone

from customersatisfactionmetrics.models import Impression, Question, Response, Survey, Touchpoint, subject_filter
from customersatisfactionmetrics.touchpoints import (
    is_eligible,
    mark_dismissed,
    mark_responded,
    record_impression,
    resolve_scope_key,
)

logger = logging.getLogger(__name__)


def scope_from_header(request):
    """
    Test scope resolver reading the scope key from a request header.
    """
    return request.META.get('HTTP_X_SCOPE', '')


class TouchpointTestCase(TestCase):
    """
    Base setup shared by the touchpoint tests.
    """

    def setUp(self):
        """
        SetUp.
        """
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='asker', password='secret')  # nosec
        self.survey = Survey.objects.create(title='Order flow', survey_type='CSAT')
        Question.objects.create(
            survey=self.survey, text='How easy was it?', response_type='INT',
            order=1, is_required=True, language='en',
        )
        Question.objects.create(
            survey=self.survey, text='What made it harder?', response_type='TEXT',
            order=2, is_required=False, language='en',
        )
        self.touchpoint = Touchpoint.objects.create(
            slug='order-placed', title='Order placed', survey=self.survey,
        )

    def make_request(self, **meta):
        """
        Build an authenticated request carrying a real session.
        """
        request = self.factory.get('/orders/', **meta)
        request.user = self.user
        self.client.force_login(self.user)
        request.session = self.client.session
        return request


class EligibilityTests(TouchpointTestCase):
    """
    Tests for the cooldown rules governing when a touchpoint may be shown.
    """

    def test_eligible_when_never_shown(self):
        """
        Eligible when never shown.
        """
        self.assertTrue(is_eligible(self.touchpoint, self.make_request()))

    def test_inactive_touchpoint_is_never_eligible(self):
        """
        Inactive touchpoint is never eligible.
        """
        self.touchpoint.is_active = False
        self.touchpoint.save()
        self.assertFalse(is_eligible(self.touchpoint, self.make_request()))

    def test_open_impression_survives_a_reload(self):
        """
        Open impression survives a reload.
        """
        request = self.make_request()
        record_impression(self.touchpoint, request)
        self.assertTrue(is_eligible(self.touchpoint, request))
        record_impression(self.touchpoint, request)
        self.assertEqual(Impression.objects.count(), 1)

    def test_dismissal_starts_the_cooldown(self):
        """
        Dismissal starts the cooldown.
        """
        request = self.make_request()
        record_impression(self.touchpoint, request)
        mark_dismissed(self.touchpoint, request)
        self.assertFalse(is_eligible(self.touchpoint, request))

    def test_response_starts_the_cooldown(self):
        """
        Response starts the cooldown.
        """
        request = self.make_request()
        record_impression(self.touchpoint, request)
        mark_responded(self.touchpoint, request)
        self.assertFalse(is_eligible(self.touchpoint, request))

    def test_eligible_again_after_the_cooldown_expires(self):
        """
        Eligible again after the cooldown expires.
        """
        request = self.make_request()
        impression = record_impression(self.touchpoint, request)
        mark_dismissed(self.touchpoint, request)
        Impression.objects.filter(pk=impression.pk).update(
            shown_at=timezone.now() - datetime.timedelta(days=self.touchpoint.cooldown_days + 1)
        )
        self.assertTrue(is_eligible(self.touchpoint, request))

    def test_global_cooldown_covers_other_touchpoints(self):
        """
        Global cooldown covers other touchpoints.
        """
        other = Touchpoint.objects.create(slug='profile-saved', title='Profile saved', survey=self.survey)
        request = self.make_request()
        record_impression(self.touchpoint, request)
        mark_dismissed(self.touchpoint, request)
        self.assertFalse(is_eligible(other, request))

    def test_touchpoint_scoped_cooldown_leaves_others_alone(self):
        """
        Touchpoint scoped cooldown leaves others alone.
        """
        other = Touchpoint.objects.create(
            slug='profile-saved', title='Profile saved', survey=self.survey,
            cooldown_scope=Touchpoint.COOLDOWN_SCOPE_TOUCHPOINT,
        )
        request = self.make_request()
        record_impression(self.touchpoint, request)
        mark_dismissed(self.touchpoint, request)
        self.assertTrue(is_eligible(other, request))

    def test_scope_cooldown_blocks_a_colleague(self):
        """
        Scope cooldown blocks a colleague.
        """
        self.touchpoint.scope_cooldown_days = 28
        self.touchpoint.save()
        colleague = get_user_model().objects.create_user(username='colleague', password='secret')  # nosec

        request = self.make_request()
        record_impression(self.touchpoint, request, scope_key='org:1')
        mark_dismissed(self.touchpoint, request)

        other_request = self.factory.get('/orders/')
        other_request.user = colleague
        self.client.force_login(colleague)
        other_request.session = self.client.session

        self.assertFalse(is_eligible(self.touchpoint, other_request, scope_key='org:1'))
        self.assertTrue(is_eligible(self.touchpoint, other_request, scope_key='org:2'))


class ScopeResolverTests(TouchpointTestCase):
    """
    Tests for resolving the scope key through the configured callable.
    """

    def test_returns_empty_without_a_resolver(self):
        """
        Returns empty without a resolver.
        """
        self.assertEqual(resolve_scope_key(self.factory.get('/')), '')

    def test_uses_the_configured_resolver(self):
        """
        Uses the configured resolver.
        """
        with self.settings(SURVEY_SCOPE_RESOLVER='customersatisfactionmetrics.tests.test_touchpoints.'
                                                 'scope_from_header'):
            request = self.factory.get('/', HTTP_X_SCOPE='org:7')
            self.assertEqual(resolve_scope_key(request), 'org:7')

    def test_a_broken_resolver_does_not_break_rendering(self):
        """
        A broken resolver does not break rendering.
        """
        with self.settings(SURVEY_SCOPE_RESOLVER='customersatisfactionmetrics.tests.does_not_exist'):
            self.assertEqual(resolve_scope_key(self.factory.get('/')), '')


class TemplateTagTests(TouchpointTestCase):
    """
    Tests for the survey_touchpoint inclusion tag.
    """

    def render(self, request, slug='order-placed'):
        """
        Render the tag for a slug and return the resulting markup.
        """
        template = Template('{% load survey_tags %}{% survey_touchpoint slug %}')
        return template.render(Context({'request': request, 'slug': slug}))

    def test_renders_the_card_and_records_an_impression(self):
        """
        Renders the card and records an impression.
        """
        html = self.render(self.make_request())
        self.assertIn('csm-touchpoint', html)
        self.assertIn('How easy was it?', html)
        self.assertIn('What made it harder?', html)
        self.assertEqual(Impression.objects.count(), 1)

    def test_renders_nothing_for_an_unknown_slug(self):
        """
        Renders nothing for an unknown slug.
        """
        self.assertEqual(self.render(self.make_request(), slug='nope').strip(), '')
        self.assertEqual(Impression.objects.count(), 0)

    def test_renders_nothing_during_a_cooldown(self):
        """
        Renders nothing during a cooldown.
        """
        request = self.make_request()
        record_impression(self.touchpoint, request)
        mark_dismissed(self.touchpoint, request)
        self.assertEqual(self.render(request).strip(), '')

    def test_optional_question_is_marked_optional(self):
        """
        Optional question is marked optional.
        """
        html = self.render(self.make_request())
        self.assertIn('Optional', html)


class TouchpointViewTests(TouchpointTestCase):
    """
    Tests for the submit and dismiss endpoints.
    """

    def test_submitting_stores_answers_and_closes_the_impression(self):
        """
        Submitting stores answers and closes the impression.
        """
        self.client.force_login(self.user)
        self.client.get('/')
        rating = self.survey.questions.get(response_type='INT')
        comment = self.survey.questions.get(response_type='TEXT')

        template = Template('{% load survey_tags %}{% survey_touchpoint "order-placed" %}')
        request = self.make_request()
        template.render(Context({'request': request}))

        response = self.client.post(
            f'/survey/touchpoint/{self.touchpoint.slug}/',
            {f'question_{rating.id}': '4', f'question_{comment.id}': 'the file kept failing', 'next': '/orders/'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/orders/')

    def test_dismissing_closes_the_impression(self):
        """
        Dismissing closes the impression.
        """
        self.client.force_login(self.user)
        request = self.make_request()
        record_impression(self.touchpoint, request)

        response = self.client.post(
            f'/survey/touchpoint/{self.touchpoint.slug}/dismiss/', {'next': '/orders/'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Impression.objects.get().dismissed_at)

    def test_submit_rejects_get(self):
        """
        Submit rejects get.
        """
        self.assertEqual(
            self.client.get(f'/survey/touchpoint/{self.touchpoint.slug}/').status_code, 405
        )

    def test_open_redirect_is_refused(self):
        """
        Open redirect is refused.
        """
        self.client.force_login(self.user)
        request = self.make_request()
        record_impression(self.touchpoint, request)
        response = self.client.post(
            f'/survey/touchpoint/{self.touchpoint.slug}/dismiss/', {'next': 'https://evil.example/'}
        )
        self.assertEqual(response['Location'], '/')


class SubjectTests(TouchpointTestCase):
    """
    Tests for linking responses and impressions to an arbitrary object.
    """

    def test_impression_records_the_subject(self):
        """
        Impression records the subject.
        """
        request = self.make_request()
        impression = record_impression(self.touchpoint, request, subject=self.survey)
        self.assertEqual(impression.content_object, self.survey)
        self.assertEqual(impression.subject, self.survey)

    def test_impression_without_a_subject_stays_blank(self):
        """
        Impression without a subject stays blank.
        """
        impression = record_impression(self.touchpoint, self.make_request())
        self.assertIsNone(impression.content_object)
        self.assertEqual(impression.object_id, '')

    def test_template_tag_passes_the_subject_through(self):
        """
        Template tag passes the subject through.
        """
        request = self.make_request()
        template = Template('{% load survey_tags %}{% survey_touchpoint "order-placed" subject=subject %}')
        template.render(Context({'request': request, 'subject': self.survey}))
        self.assertEqual(Impression.objects.get().content_object, self.survey)

    def test_answers_inherit_the_subject_from_the_impression(self):
        """
        Answers inherit the subject from the impression.
        """
        self.client.force_login(self.user)
        rating = self.survey.questions.get(response_type='INT')

        request = self.make_request()
        template = Template('{% load survey_tags %}{% survey_touchpoint "order-placed" subject=subject %}')
        template.render(Context({'request': request, 'subject': self.survey}))

        self.client.post(
            f'/survey/touchpoint/{self.touchpoint.slug}/',
            {f'question_{rating.id}': '5', 'next': '/orders/'},
        )
        response = Response.objects.get(question=rating)
        self.assertEqual(response.content_object, self.survey)

    def test_subject_filter_finds_feedback_about_an_object(self):
        """
        Subject filter finds feedback about an object.
        """
        request = self.make_request()
        record_impression(self.touchpoint, request, subject=self.survey)
        self.assertEqual(Impression.objects.filter(**subject_filter(self.survey)).count(), 1)

    def test_a_deleted_subject_leaves_the_answer_readable(self):
        """
        A deleted subject leaves the answer readable.
        """
        impression = record_impression(self.touchpoint, self.make_request(), subject=self.survey)
        self.assertEqual(impression.object_id, str(self.survey.pk))
        self.assertEqual(impression.content_type.model, 'survey')
