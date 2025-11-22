from rest_framework import serializers
from .models import CartItem
from Products.serializers import ProductSerializer  # agar mahsulotning ma'lumotlarini ham ko'rsatmoqchi bo'lsak

class CartItemSerializer(serializers.ModelSerializer):
    # Product ma'lumotlarini nested ko'rsatish (optional)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=CartItem.objects.model.product.field.related_model.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'author', 'product', 'product_id', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def create(self, validated_data):
        # author ni request user orqali o'rnatamiz
        user = self.context['request'].user
        validated_data['author'] = user
        # agar savatda bu mahsulot allaqachon bo'lsa, quantity ni oshiramiz
        cart_item, created = CartItem.objects.get_or_create(
            author=user,
            product=validated_data['product'],
            defaults={'quantity': validated_data.get('quantity', 1)}
        )
        if not created:
            cart_item.quantity += validated_data.get('quantity', 1)
            cart_item.save()
        return cart_item
