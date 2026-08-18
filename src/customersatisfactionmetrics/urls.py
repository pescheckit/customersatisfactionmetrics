"""
URL Configuration for the Customer Satisfaction Metrics application.

This module defines the URL routes for the Customer Satisfaction Metrics application,
including paths for accessing surveys by slug and survey IDs (if enabled in settings),
the touchpoint submit and dismiss endpoints, and the thank-you page after survey
submission.
"""

from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    # Path to access survey by Slug
    path('survey/slug/<slug:slug>/', views.survey_view, {'survey_id': None}, name='survey_view_by_slug'),
    path('survey/thank-you/', views.thank_you_view, name='thank_you'),
    # Touchpoints embedded in the host application's own pages
    path('survey/touchpoint/<slug:slug>/', views.touchpoint_submit_view, name='touchpoint_submit'),
    path('survey/touchpoint/<slug:slug>/dismiss/', views.touchpoint_dismiss_view, name='touchpoint_dismiss'),
]

# Conditionally add URL pattern for accessing survey by ID based on settings
if getattr(settings, 'SURVEY_ENABLE_ID_URL', False):
    urlpatterns.append(path('survey/id/<int:survey_id>/', views.survey_view, name='survey_view_by_id'))
