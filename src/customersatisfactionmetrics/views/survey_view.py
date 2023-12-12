"""
View module for handling survey-related views in the Customer Satisfaction Metrics application.

This module includes views to display and process survey forms, as well as utilities
for extracting client IP information from requests.
"""

from django.http import Http404
from django.shortcuts import redirect, render

from customersatisfactionmetrics.forms.survey_form import SurveyForm
from customersatisfactionmetrics.models import Question, Response, Survey


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
    # Fetch the survey by ID or slug
    if survey_id:
        survey = Survey.objects.get(pk=survey_id)
    elif slug:
        survey = Survey.objects.get(slug=slug)
    else:
        raise Http404("Survey not found")

    if request.method == 'POST':
        form = SurveyForm(request.POST, survey_id=survey_id, slug=slug)
        if form.is_valid():
            session_id = request.session.session_key or generate_unique_session_id(request)
            for key, value in form.cleaned_data.items():
                if key.startswith('question_'):
                    question_id = int(key.split('_')[1])
                    question = Question.objects.get(pk=question_id)
                    response_type = survey.survey_type
                    client_ip = get_client_ip(request)

                    # Check for existing response
                    existing_response = Response.objects.filter(
                        question=question,
                        session_id=session_id
                    ).first()

                    if existing_response:
                        existing_response.text = value
                        existing_response.save()
                    else:
                        Response.objects.create(
                            user=request.user if request.user.is_authenticated else None,
                            question=question,
                            text=value,
                            response_type=response_type,
                            ip_address=client_ip,
                            user_agent=request.META.get('HTTP_USER_AGENT'),
                            session_id=session_id
                        )
            return redirect('thank_you')
    else:
        form = SurveyForm(survey_id=survey_id, slug=slug)

    return render(request, 'survey_form.html', {'form': form, 'survey': survey})


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
