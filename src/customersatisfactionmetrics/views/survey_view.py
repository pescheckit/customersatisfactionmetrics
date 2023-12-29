"""
View module for handling survey-related views in the Customer Satisfaction Metrics application.

This module includes views to display and process survey forms, as well as utilities
for extracting client IP information from requests.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import redirect, render

from customersatisfactionmetrics.forms.survey_form import SurveyForm
from customersatisfactionmetrics.models import Question, Survey


def survey_view(request, survey_id=None, slug=None):
    """
    View for displaying and processing a survey form.

    Fetches a survey either by its ID or slug and displays its form. Handles the
    submission of the form and creation of response records.

    Args:
        request: The HttpRequest object.
        survey_id (int, optional): The ID of the survey to be displayed.
        slug (str, optional): The slug of the survey to be displayed.

    Returns:
        HttpResponse: The rendered survey form or a redirect to a thank you page.
    """
    if survey_id:
        survey = Survey.objects.get(pk=survey_id)
    elif slug:
        survey = Survey.objects.get(slug=slug)
    else:
        raise Http404("Survey not found")

    form_submitted = False
    if request.method == 'POST':
        form = SurveyForm(
            request.POST,
            survey_id=survey_id,
            slug=slug,
            session_id=generate_unique_session_id(request)
        )
        if form.is_valid():
            if getattr(settings, 'SURVEY_SELF_POST', False):
                process_form_submission(request, form, survey)
                form_submitted = True
            else:
                return redirect('thank_you')
    else:
        form = SurveyForm(
            survey_id=survey_id,
            slug=slug,
            session_id=generate_unique_session_id(request)
        )

    return render(request, 'survey_form.html', {
        'form': form,
        'survey': survey,
        'form_submitted': form_submitted
    })


def process_form_submission(request, form, survey):
    """
    Processes the form submission for a survey.

    Args:
        request: The HttpRequest object.
        form: The submitted SurveyForm.
        survey: The Survey instance related to the form.
    """
    for key, value in form.cleaned_data.items():
        if key.startswith('question_'):
            form.save(**get_form_kwargs(request, key, value, survey))


def get_form_kwargs(request, key, value, survey):
    """
    Construct and return keyword arguments for saving form data.

    This function generates and organizes keyword arguments required for saving
    survey form data, including user, question, text response, response type,
    IP address, user agent, and session ID.

    Args:
        request: The HttpRequest object.
        key (str): The key associated with the question in the form data.
        value: The submitted value for the question.
        survey: The Survey instance related to the form.

    Returns:
        dict: A dictionary containing keyword arguments for saving form data.
    """
    session_id = request.session.session_key or generate_unique_session_id(request)
    question_id = int(key.split('_')[1])
    question = Question.objects.get(pk=question_id)
    response_type = survey.survey_type
    client_ip = get_client_ip(request)

    user = None
    if isinstance(request.user, get_user_model()):
        user = request.user

    return {
        'user': user,
        'question': question,
        'text': value,
        'response_type': response_type,
        'ip_address': client_ip,
        'user_agent': request.META.get('HTTP_USER_AGENT'),
        'session_id': session_id
    }


def generate_unique_session_id(request):
    """
    Retrieve or create a unique session ID for the user.

    If the user does not already have a session, this function creates a new session.
    It ensures that each user, whether authenticated or anonymous, has a unique session ID.

    Args:
        request: The HttpRequest object from Django.

    Returns:
        str: A unique session key for the user's session.
    """
    if not request.session.exists(request.session.session_key):
        request.session.create()
    return request.session.session_key


def get_client_ip(request):
    """
    Get the client's IP address from a Django request.

    Args:
        request: The HttpRequest object.

    Returns:
        str: The IP address of the client.
    """
    headers = [
        'X-REAL-IP',  # Alternative real IP header
        'CF-Connecting-IP',  # Cloudflare header
        'HTTP_X_FORWARDED_FOR',
        'HTTP_CLIENT_IP',
        'HTTP_X_REAL_IP',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'HTTP_VIA',
    ]

    for header in headers:
        ip = request.META.get(header)
        if ip:
            if header == 'HTTP_X_FORWARDED_FOR':
                ip = ip.split(',')[0]
            return ip.strip()

    return request.META.get('REMOTE_ADDR')
