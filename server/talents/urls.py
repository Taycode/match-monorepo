from .views import AddToTalentPoolViewSet
from django.urls import path


urlpatterns = [
    path('add-to-pool', AddToTalentPoolViewSet.as_view(), name='add-to-talent-pool'),
]
