from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import TalentDocumentViewSet

router = DefaultRouter()
router.register(r'talents', TalentDocumentViewSet, basename='talentdocument')

