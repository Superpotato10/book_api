from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from books.models import Author
from books.serializers import AuthorSerializer
from common.permissions import ReadOnly, IsManager


@extend_schema(tags=['Authors'])
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [ReadOnly | (IsAuthenticated & IsManager)]
