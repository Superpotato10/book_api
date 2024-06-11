from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from books.models import Book
from books.serializers import BookSerializer
from common.permissions import ReadOnly, IsManager


@extend_schema(tags=['Books'])
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [ReadOnly | (IsAuthenticated & IsManager)]
