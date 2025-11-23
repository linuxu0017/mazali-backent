from django.urls import path
from .views import (
    RegisterDeviceView,
    NotificationListCreateView,
    MarkNotificationAsReadView,
    AdminSendNotificationView
)

urlpatterns = [
    path("register-device/", RegisterDeviceView.as_view(), name="device-register"),
    path("notification/", NotificationListCreateView.as_view(), name="notification-list-create"),
    path("notification/<int:pk>/read/", MarkNotificationAsReadView.as_view(), name="notification-mark-read"),
    path("notification/send/", AdminSendNotificationView.as_view(), name="admin-send-notification"),
]
