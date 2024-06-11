from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from books.models import Publisher
from books.serializers import PublisherSerializer
from common.permissions import IsManager, ReadOnly


@extend_schema(tags=['Publisher'])
class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [ReadOnly | (IsAuthenticated & IsManager)]
