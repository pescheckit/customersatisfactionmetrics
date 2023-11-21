from django.contrib import admin

from .models import Question, Response, Survey

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey', 'order', 'response_type')  # Add other relevant fields here
    list_editable = ('order',)  # Allow 'order' to be editable in the list view
    ordering = ('survey', 'order')  # Order by survey first, then by question order

    # Optionally, you can add a search field or filters if you have many questions
    search_fields = ['text']
    list_filter = ['survey']


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'response_type', 'shortened_text', 'ip_address', 'user_agent')
    list_filter = ('response_type', 'user', 'question__survey')
    search_fields = ('text', 'user__username', 'question__text')
    readonly_fields = ('ip_address', 'user_agent')  # Assuming these shouldn't be editable

    def shortened_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    shortened_text.short_description = 'Response Text'


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'survey_type', 'created_at', 'slug')
    list_filter = ('survey_type', 'created_at')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}  # Automatically fill the slug field from the title
    readonly_fields = ('created_at',)  # Assuming created_at should not be editable


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Question, QuestionAdmin)