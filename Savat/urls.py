from django.urls import path
from .views import CartView

urlpatterns = [
    path('basket/', CartView.as_view(), name='cart'),
    path('basket/<int:pk>/', CartView.as_view(), name='cart-detail'),  # PUT va DELETE uchun
]
