from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from .models import Talent
# from talents.documents import TalentDocument
import cloudinary.uploader


# class TalentDocumentSerializer(DocumentSerializer):
#     """Serializer for the talent document"""
#
#     class Meta:
#         """Meta options."""
#
#         document = TalentDocument
#
#         fields = (
#             'id',
#             'skills',
#             'role',
#             'years_of_experience'
#         )


class TalentPoolSerializer(serializers.ModelSerializer):
    resume_file = serializers.FileField(write_only=True)

    class Meta:
        model = Talent
        fields = [
            'first_name',
            'last_name',
            'role',
            'phone_number',
            'email',
            'years_of_experience',
            'resume_file',
            'resume'
        ]
        read_only_fields = ['resume']

    def create(self, validated_data):
        # Extract the file and other data
        file = validated_data.pop('resume_file')
        # Upload the file to Cloudinary
        result = cloudinary.uploader.upload(file, resource_type="raw")
        # Save the URL in the model
        validated_data['resume'] = result.get('url')
        return super().create(validated_data)
