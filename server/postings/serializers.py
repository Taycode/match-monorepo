from rest_framework import serializers

from postings.models import Posting, Job, FormResponse, Match


class PostingSerializer(serializers.ModelSerializer):
    edited_tweet = serializers.CharField(required=False)
    generated_tweet = serializers.CharField(required=True)

    @staticmethod
    def validate_edited_tweet(value):
        # Let's assume value is a string
        if value:
            from .utils import tweet_length_with_shortened_links

            if tweet_length_with_shortened_links(value) > 240:
                raise serializers.ValidationError(
                    "Edited tweet exceeds the 240-character limit when shortened links are considered."
                )
        return value

    class Meta:
        model = Posting
        fields = '__all__'


class InitiatePostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = ['source', 'post']


# MVP Job Serializers
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 
            'google_form_id', 'google_form_url',
            'google_sheet_id', 'google_sheet_url',
            'twitter_post_id', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'google_form_id', 'google_form_url',
            'google_sheet_id', 'google_sheet_url',
            'twitter_post_id', 'created_at', 'updated_at'
        ]


class CreateJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'description']


class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormResponse
        fields = [
            'id', 'job', 'name', 'email', 'resume_url', 
            'response_data', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MatchSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()
    candidate_email = serializers.SerializerMethodField()
    candidate_resume_url = serializers.SerializerMethodField()
    candidate_skills = serializers.SerializerMethodField()
    
    class Meta:
        model = Match
        fields = [
            'id', 'job', 'candidate_id', 'candidate_type',
            'similarity_score', 'is_shortlisted', 'created_at',
            'candidate_name', 'candidate_email', 'candidate_resume_url', 'candidate_skills'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_candidate_name(self, obj):
        if obj.candidate_type == 'talent':
            from talents.models import Talent
            try:
                talent = Talent.objects.get(id=obj.candidate_id)
                return f"{talent.first_name} {talent.last_name}"
            except Talent.DoesNotExist:
                return None
        elif obj.candidate_type == 'form_response':
            try:
                form_response = FormResponse.objects.get(id=obj.candidate_id)
                return form_response.name
            except FormResponse.DoesNotExist:
                return None
        return None
    
    def get_candidate_email(self, obj):
        if obj.candidate_type == 'talent':
            from talents.models import Talent
            try:
                talent = Talent.objects.get(id=obj.candidate_id)
                return talent.email
            except Talent.DoesNotExist:
                return None
        elif obj.candidate_type == 'form_response':
            try:
                form_response = FormResponse.objects.get(id=obj.candidate_id)
                return form_response.email
            except FormResponse.DoesNotExist:
                return None
        return None
    
    def get_candidate_resume_url(self, obj):
        if obj.candidate_type == 'talent':
            from talents.models import Talent
            try:
                talent = Talent.objects.get(id=obj.candidate_id)
                return talent.resume_url
            except Talent.DoesNotExist:
                return None
        elif obj.candidate_type == 'form_response':
            try:
                form_response = FormResponse.objects.get(id=obj.candidate_id)
                return form_response.resume_url
            except FormResponse.DoesNotExist:
                return None
        return None
    
    def get_candidate_skills(self, obj):
        if obj.candidate_type == 'talent':
            from talents.models import Talent
            try:
                talent = Talent.objects.get(id=obj.candidate_id)
                return talent.skills
            except Talent.DoesNotExist:
                return None
        elif obj.candidate_type == 'form_response':
            try:
                form_response = FormResponse.objects.get(id=obj.candidate_id)
                # Extract skills from response_data if available
                return form_response.response_data.get('skills', [])
            except FormResponse.DoesNotExist:
                return None
        return None
