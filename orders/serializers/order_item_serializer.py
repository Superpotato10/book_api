from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from orders.models import OrderItem


class CreateOrderItemSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = OrderItem
        fields = ('book', 'quantity')


class ReadOrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('book', 'quantity')
