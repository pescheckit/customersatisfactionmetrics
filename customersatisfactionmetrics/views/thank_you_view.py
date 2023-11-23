"""
View module for the thank-you page in the Customer Satisfaction Metrics application.

This module contains the view for rendering the thank-you page displayed after a user
submits a survey response.
"""

from django.shortcuts import render


def thank_you_view(request):
    """
    View for displaying the thank-you page.

    Renders the thank-you page template after a survey response has been submitted.

    Args:
        request: The HttpRequest object.

    Returns:
        HttpResponse: The rendered thank-you page.
    """
    return render(request, 'thank_you.html')
