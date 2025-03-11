from rest_framework import generics
from .models import Posting
from .pagination import PostingCursorPagination
from .serializers import PostingSerializer, InitiatePostingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
import structlog
from .services import generate_tweet_content_for_posting, trigger_post_on_twitter
from djangorestframework_camel_case.parser import CamelCaseJSONParser

logger = structlog.get_logger(__name__)


class CreatePostingView(generics.CreateAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    parser_classes = [CamelCaseJSONParser]

    def create(self, request, *args, **kwargs):
        """
        We override `create` to add custom error handling/logging.
        Note that `super().create(...)` returns a `Response`, not the instance.
        """
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            # Re-raise validation errors to return the usual 400 response
            raise e from e
        except Exception:
            # Log any unexpected error and return a generic 500
            logger.exception("Error creating Posting or posting tweet on Twitter")
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        """
        This is where the actual instance is created.
        We call `serializer.save()` to create the object,
        then run `trigger_post_on_twitter(...)` with the newly created instance.
        """
        instance = serializer.save()
        trigger_post_on_twitter(instance)


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
