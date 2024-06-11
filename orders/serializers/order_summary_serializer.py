from rest_framework import serializers


class OrderSummarySerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    total_earnings = serializers.IntegerField()
