from rest_framework import serializers
from .models import Order, OrderItem
from Products.models import Product
from Products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'comment']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'author', 'status', 'created_at', 'lat', 'long', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        author = validated_data.pop('author', None)
        order = Order.objects.create(author=author, **validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.long = validated_data.get('long', instance.long)
        instance.save()
        return instance
