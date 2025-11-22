from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from Savat.models import CartItem  # Savatdagi mahsulotlar

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Userning barcha buyurtmalarini olish"""
        orders = Order.objects.filter(author=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """User buyurtma yaratadi, savatdagi mahsulotlar avtomatik olinadi"""
        user = request.user
        lat = request.data.get('lat')
        long = request.data.get('long')

        if lat is None or long is None:
            return Response({"error": "Latitude and longitude are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Userning savatidagi barcha mahsulotlarni olish
        cart_items = CartItem.objects.filter(author=user)
        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Buyurtma yaratish
        order = Order.objects.create(author=user, lat=lat, long=long)

        # Savatdagi har bir mahsulot asosida OrderItem yaratish
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # Savatni bo'shatish
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        """Buyurtma holatini yangilash (masalan, admin tomonidan holatni update qilish)"""
        try:
            order = Order.objects.get(pk=pk, author=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        """Buyurtmani bekor qilish faqat 'Tayyorlanmoqda' holatida mumkin"""
        try:
            order = Order.objects.get(pk=pk, author=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status == 'pending':
            order.delete()
            return Response({"success": "Order canceled"}, status=status.HTTP_204_NO_CONTENT)

        elif order.status != 'pending':
            return Response({"error": "Cannot cancel an order that is in progress"},status=status.HTTP_400_BAD_REQUEST)

