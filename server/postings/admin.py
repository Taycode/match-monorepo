from django.contrib import admin

from postings.models import Posting, Job, FormResponse, Match

# Register your models here.
admin.site.register(Posting)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'google_form_url', 'google_sheet_url', 'twitter_post_id']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Job Details', {
            'fields': ('title', 'description')
        }),
        ('Automation Links', {
            'fields': ('google_form_id', 'google_form_url', 'google_sheet_id', 'google_sheet_url', 'twitter_post_id')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )


@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'job', 'created_at']
    list_filter = ['created_at', 'job']
    search_fields = ['name', 'email', 'job__title']
    readonly_fields = ['id', 'created_at']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['job', 'candidate_type', 'similarity_score', 'is_shortlisted', 'created_at']
    list_filter = ['candidate_type', 'is_shortlisted', 'created_at']
    search_fields = ['job__title']
    readonly_fields = ['id', 'created_at']
