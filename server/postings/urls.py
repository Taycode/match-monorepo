from django.urls import path
from .views import (
    # Existing social media posting views
    CreatePostingView, InitiatePostingView, RetrievePostingView, ListPostingView,
    # New MVP job posting views
    CreateJobView, ListJobsView, JobDetailView, JobMatchesView,
    ShortlistCandidateView, RefreshMatchesView, JobStatsView, SyncFormResponsesView
)

urlpatterns = [
    # Existing social media posting URLs
    path('create', CreatePostingView.as_view(), name='create_posting'),
    path('initiate', InitiatePostingView.as_view(), name='initiate_posting'),
    path('view/<str:pk>', RetrievePostingView.as_view(), name='retrieve_posting'),
    path('list', ListPostingView.as_view(), name='list_posting'),
    
    # MVP Job Posting URLs
    path('jobs/', CreateJobView.as_view(), name='create_job'),
    path('jobs/list/', ListJobsView.as_view(), name='list_jobs'),
    path('jobs/<str:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/<str:job_id>/matches/', JobMatchesView.as_view(), name='job_matches'),
    path('jobs/<str:job_id>/refresh-matches/', RefreshMatchesView.as_view(), name='refresh_matches'),
    path('jobs/<str:job_id>/stats/', JobStatsView.as_view(), name='job_stats'),
    path('jobs/<str:job_id>/sync-responses/', SyncFormResponsesView.as_view(), name='sync_form_responses'),
    path('matches/<str:match_id>/shortlist/', ShortlistCandidateView.as_view(), name='shortlist_candidate'),
]
