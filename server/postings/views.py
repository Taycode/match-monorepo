from rest_framework import generics
from .models import Posting
from .serializers import PostingSerializer


class CreatePostingView(generics.CreateAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
