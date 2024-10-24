"""
Admin configuration for the Customer Satisfaction Metrics Django app.

This module defines the Django administration interface for the models in the
Customer Satisfaction Metrics app. It customizes how models are displayed and
handled in the Django admin site, including list views, filters, and search capabilities.
"""
from django.contrib import admin

from .models import Question, Response, Survey


class QuestionAdmin(admin.ModelAdmin):
    """
    Administration interface for the Question model.
    Includes configurations for display and editing in the Django admin site.
    """

    list_display = ('text', 'language', 'survey', 'order', 'response_type', 'is_required', 'min_label', 'max_label')
    list_editable = ('order', 'is_required')
    ordering = ('survey', 'order')
    search_fields = ['text']
    list_filter = ['survey', 'response_type', 'is_required']


class ResponseAdmin(admin.ModelAdmin):
    """
    Administration interface for the Response model.
    Provides a customized view in the admin interface, including display formatting
    and filtering options.
    """

    list_display = ('question', 'user', 'response_type', 'shortened_text', 'ip_address', 'user_agent', 'session_id')
    list_filter = ('response_type', 'user', 'question__survey')
    search_fields = ('text', 'user__username', 'question__text')
    readonly_fields = ('ip_address', 'user_agent')

    def shortened_text(self, obj):
        """
        Returns a shortened version of the response text for display in the admin interface.

        Args:
            obj (Response): The Response object.

        Returns:
            str: The shortened text of the response.
        """
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    shortened_text.short_description = 'Response Text'


class SurveyAdmin(admin.ModelAdmin):
    """
    Administration interface for the Survey model.
    Configures list display, search capabilities, and other options for managing Surveys
    in the admin interface.
    """

    list_display = ('title', 'survey_type', 'created_at', 'slug')
    list_filter = ('survey_type', 'created_at')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at',)


# Registering the admin classes with the associated models
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Question, QuestionAdmin)
