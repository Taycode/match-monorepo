from django.urls import path
from .views import CreatePostingView

urlpatterns = [
    path('create', CreatePostingView.as_view(), name='create_posting'),
]
