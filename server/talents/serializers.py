from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from talents.documents import TalentDocument


class TalentDocumentSerializer(DocumentSerializer):
    """Serializer for the talent document"""

    class Meta:
        """Meta options."""

        document = TalentDocument

        fields = (
            'id',
            'skills',
            'role',
            'years_of_experience'
        )
