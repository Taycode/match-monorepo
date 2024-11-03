from rest_framework import serializers

from postings.models import Posting


class PostingSerializer(serializers.ModelSerializer):
    editedTweet = serializers.CharField(source='edited_tweet', required=False)
    generatedTweet = serializers.CharField(source='generated_tweet', required=True)

    class Meta:
        model = Posting
        exclude = ['edited_tweet', 'generated_tweet']


class InitiatePostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = ['source', 'post']
