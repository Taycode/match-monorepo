from talents.models import Talent
from talents.serializers import TalentPoolSerializer
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class AddToTalentPoolViewSet(CreateAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentPoolSerializer
    parser_classes = [MultiPartParser, FormParser]  # To handle multipart/form-data

    @swagger_auto_schema(
        operation_description="Endpoint to add a talent to the pool with multipart/form-data.",
        consumes=["multipart/form-data"],  # Explicitly set content type
        manual_parameters=[
            openapi.Parameter(
                'first_name', openapi.IN_FORM, description='First name of the talent', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'last_name', openapi.IN_FORM, description='Last name of the talent', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'role', openapi.IN_FORM, description='Role of the talent', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'phone_number', openapi.IN_FORM, description='Phone number of the talent', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'email', openapi.IN_FORM, description='Email address of the talent', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'years_of_experience', openapi.IN_FORM, description='Years of experience', type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'resume_file', openapi.IN_FORM, description='Resume file to upload', type=openapi.TYPE_FILE
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        except ValidationError as err:
            return Response({
                "errors": err.detail,
                "message": "Validation error"
            },
                status=422
            )
