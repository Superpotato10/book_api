from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.models import Order, OrderItem
from .order_item_serializer import CreateOrderItemSerializer, ReadOrderItemSerializer


class CreateOrderSerializer(serializers.ModelSerializer):
    items = CreateOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'address', 'items')

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.create(user=user,
                                     address=validated_data['address'])

        for item in validated_data['items']:
            OrderItem.objects.create(order=order,
                                     user=user,
                                     quantity=item['quantity'],
                                     book=item['book'])

        return order

    def validate_items(self, value):
        if len(value) == 0:
            raise ValidationError('Field items should not be empty list')

        return value


class ReadOrderSerializer(serializers.ModelSerializer):
    items = ReadOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'address', 'items')
