from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import AddToTalentPoolViewSet
from django.urls import path

router = DefaultRouter()
# router.register(r'talents', TalentDocumentViewSet, basename='talentdocument')

urlpatterns = [
    path('', include(router.urls)),
    path('add-to-pool', AddToTalentPoolViewSet.as_view(), name='add-to-talent-pool'),
]
