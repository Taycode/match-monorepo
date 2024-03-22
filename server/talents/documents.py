from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from talents.models import Talent


@registry.register_document
class TalentDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'talents'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Talent
        fields = ['skills', 'role', 'years_of_experience']
