from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from talents.documents import TalentDocument
from talents.filter_backend import KeywordParserFilterBackend
from talents.serializers import TalentDocumentSerializer
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)


class TalentDocumentViewSet(BaseDocumentViewSet):
    document = TalentDocument
    serializer_class = TalentDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = (KeywordParserFilterBackend, )
    # search_fields = (
    #     'id',
    #     'skills',
    #     'role',
    #     'years_of_experience',
    # )
    # filter_fields = {
    #     'id': 'id',
    #     'role': 'role.raw',
    #     'years_of_experience': {
    #         'field': 'years_of_experience.raw',
    #         'lookups': [
    #             LOOKUP_FILTER_RANGE,
    #             LOOKUP_QUERY_GT,
    #             LOOKUP_QUERY_GTE,
    #             LOOKUP_QUERY_LT,
    #             LOOKUP_QUERY_LTE,
    #         ]
    #     }
    # }
    # ordering_fields = {
    #     'id': 'id',
    #     'role': 'role.raw',
    #     'years_of_experience': 'years_of_experience.raw',
    # }
    # ordering = ('id', 'role', 'years_of_experience')
    #

