from django.urls import path
from .views import CreatePostingView, InitiatePostingView, RetrievePostingView, ListPostingView

urlpatterns = [
    path('create', CreatePostingView.as_view(), name='create_posting'),
    path('initiate', InitiatePostingView.as_view(), name='initiate_posting'),
    path('view/<str:pk>', RetrievePostingView.as_view(), name='retrieve_posting'),
    path('list', ListPostingView.as_view(), name='list_posting')
]
