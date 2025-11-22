from django.db import models
from Users.models import CustomUser
from Products.models import Product
from Savat.models import CartItem  # Agar CartItem snapshot sifatida ishlatilsa

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Tayyorlanmoqda'),
        ('delivering', 'Yetkazib berilyapti'),
        ('received', 'Qabul qilindi'),
        ('accepted', 'Qabul qilb olish'),
    ]

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.author}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True, null=True)  # optional, agar kerak bo‘lsa

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"
