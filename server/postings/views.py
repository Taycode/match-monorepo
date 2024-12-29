from rest_framework import generics
from .models import Posting
from .pagination import PostingCursorPagination
from .serializers import PostingSerializer, InitiatePostingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import generate_tweet_content_for_posting


class CreatePostingView(generics.CreateAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer


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
