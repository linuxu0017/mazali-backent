from django.urls import path
from .views import OrderView

urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),                    # Yangi buyurtma yaratish va ro'yxat
    path('order/<int:pk>/', OrderView.as_view(), name='order-detail'),    # PUT va DELETE uchun pk kerak
]
