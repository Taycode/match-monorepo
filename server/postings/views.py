from rest_framework import generics
from .models import Posting
from .pagination import PostingCursorPagination
from .serializers import PostingSerializer, InitiatePostingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import structlog
from .services import generate_tweet_content_for_posting, trigger_post_on_twitter

logger = structlog.get_logger(__name__)


class CreatePostingView(generics.CreateAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

    def post(self, request, *args, **kwargs):
        try:
            instance = super().post(request, *args, **kwargs)
            trigger_post_on_twitter(instance)
            return instance
        except Exception as e:
            logger.error("Error posting tweet on twitter", exc=e)
            return Response({
                'message': 'An error occurred'
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetrievePostingView(generics.RetrieveAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer


class ListPostingView(generics.ListAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    pagination_class = PostingCursorPagination


class InitiatePostingView(APIView):
    serializer_class = InitiatePostingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        responses = generate_tweet_content_for_posting(
            validated_data,
            2
        )
        return Response({
            'responses': responses
        }, status.HTTP_200_OK)
