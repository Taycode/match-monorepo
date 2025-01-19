from rest_framework import serializers

from postings.models import Posting


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
