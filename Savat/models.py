# Cart/models.py
from django.db import models
from Users.models import CustomUser  # siz yaratgan custom user modeli
from Products.models import Product

class CartItem(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # minimal 1 ta

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('author', 'product')  # bir user bir mahsulotni bir necha marta alohida yozuv sifatida qo‘sholmasin

    def __str__(self):
        return f"{self.author} - {self.product.name} ({self.quantity})"
