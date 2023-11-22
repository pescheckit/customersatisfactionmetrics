from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    # Path to access survey by Slug
    path('survey/slug/<slug:slug>/', views.survey_view, {'survey_id': None}, name='survey_view_by_slug'),
    path('survey/thank-you/', views.thank_you_view, name='thank_you'),
]

if getattr(settings, 'SURVEY_ENABLE_ID_URL', False):
    urlpatterns.append(path('survey/id/<int:survey_id>/', views.survey_view, name='survey_view_by_id'))
