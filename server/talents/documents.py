from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from talents.models import Talent


@registry.register_document
class TalentDocument(Document):
    skills = fields.TextField(attr='skills_list_method')

    class Index:
        # Name of the Elasticsearch index
        name = 'talents'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Talent
        fields = ['id', 'first_name', 'last_name', 'role', 'years_of_experience']

    def skills_list_method(self, instance: Talent):
        return instance.skills
