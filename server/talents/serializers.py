from rest_framework import serializers
from .models import Talent
import cloudinary.uploader


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
