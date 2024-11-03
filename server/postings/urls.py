from django.urls import path
from .views import CreatePostingView, InitiatePostingView

urlpatterns = [
    path('create', CreatePostingView.as_view(), name='create_posting'),
    path('initiate', InitiatePostingView.as_view(), name='initiate_posting'),
]
