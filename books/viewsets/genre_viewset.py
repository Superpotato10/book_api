from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from books.models import Genre
from books.serializers import GenreSerializer
from common.permissions import IsManager, ReadOnly


@extend_schema(tags=['Genres'])
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | (IsAuthenticated & IsManager)]
