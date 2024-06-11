from django.db.models import Sum, F
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from common.permissions import IsManager
from orders.models import Order, OrderItem
from orders.permissions import IsOrderOwner
from orders.serializers import CreateOrderSerializer, OrderStatusSerializer, OrderSummarySerializer
from orders.serializers.order_serializer import ReadOrderSerializer


@extend_schema(tags=['Orders'])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated & IsOrderOwner]

    @extend_schema(parameters=[OpenApiParameter('client_id', OpenApiTypes.INT, OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(responses={200: OrderSummarySerializer})
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated & IsManager])
    def summary(self, *args, **kwargs):
        serializer = OrderSummarySerializer({
            'total_orders': Order.objects.all().count(),
            'total_earnings': OrderItem.objects.annotate(
                total_price=F('quantity') * F('book__price')
            ).aggregate(total=Sum('total_price'))['total']
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: OrderStatusSerializer})
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated & IsManager])
    def status(self, *args, **kwargs):
        serializer = OrderStatusSerializer({
            'pending_orders': Order.objects.filter(status=Order.Status.PENDING).count(),
            'shipped_orders': Order.objects.filter(status=Order.Status.SHIPPED).count(),
            'delivered_orders': Order.objects.filter(status=Order.Status.DELIVERED).count()
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        client_id = self.request.query_params.get('client_id', None)

        if user.is_manager:
            return Order.objects.filter(user_id=client_id) if client_id else Order.objects.all()

        return Order.objects.filter(user_id=user.id)

    def get_serializer_class(self):
        return ReadOrderSerializer if self.request.method in SAFE_METHODS else CreateOrderSerializer
