from rest_framework import serializers
from .models import Talent
import cloudinary.uploader
from rest_framework.exceptions import ValidationError

from .service import post_process_new_talent


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
            'resume_url'
        ]
        read_only_fields = ['resume_url']

    def create(self, validated_data):
        # Extract the file and other data
        email = validated_data.get('email')
        if Talent.objects.filter(email=email).exists():
            raise ValidationError({"email": "A talent with this email already exists."})
        file = validated_data.pop('resume_file')
        # Upload the file to Cloudinary
        result = cloudinary.uploader.upload(file, resource_type="raw")
        # Save the URL in the model
        validated_data['resume_url'] = result.get('url')
        talent = super().create(validated_data)
        post_process_new_talent(talent)
        return talent
