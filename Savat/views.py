from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CartItem
from .serializers import CartItemSerializer

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Faqat ro'yxatdan o'tgan userlar

    def get(self, request):
        """
        User o'z savatidagi barcha mahsulotlarni ko'radi
        """
        cart_items = CartItem.objects.filter(author=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Savatga yangi mahsulot qo'shish yoki mavjud bo'lsa quantity ni oshirish
        """
        serializer = CartItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.save()
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        Savatdagi mahsulot quantity ni yangilash
        """
        try:
            cart_item = CartItem.objects.get(pk=pk, author=request.user)  # pk = CartItem ID
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity')
        if quantity is not None and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data)
        else:
            return Response({"detail": "Invalid quantity."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Savatdagi mahsulotni o'chirish
        """
        try:
            cart_item = CartItem.objects.get(pk=pk, author=request.user)  # pk = CartItem ID
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

