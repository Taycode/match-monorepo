from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from talents.documents import TalentDocument
from talents.filter_backend import KeywordParserFilterBackend
from talents.serializers import TalentDocumentSerializer


class TalentDocumentViewSet(BaseDocumentViewSet):
    document = TalentDocument
    serializer_class = TalentDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = (KeywordParserFilterBackend, )
