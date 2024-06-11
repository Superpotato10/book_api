from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from common.serializers import UserSerializer

UserModel = get_user_model()


@extend_schema(tags=['Authorization'])
class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
