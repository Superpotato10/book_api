from rest_framework import serializers


class OrderStatusSerializer(serializers.Serializer):
    pending_orders = serializers.IntegerField()
    shipped_orders = serializers.IntegerField()
    delivered_orders = serializers.IntegerField()
