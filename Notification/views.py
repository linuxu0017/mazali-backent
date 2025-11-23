from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification, DeliveryLog, Device
from .serializers import NotificationSerializer, DeliveryLogSerializer, DeviceSerializer

# ---------------- Device ----------------
class RegisterDeviceView(generics.CreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ---------------- Notifications ----------------
class NotificationListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Foydalanuvchiga yuborilgan notificationlar
        return DeliveryLog.objects.filter(user=self.request.user).select_related('notification').order_by('-notification__created_at')

    def perform_create(self, serializer):
        # Test uchun oddiy user ham notification yaratishi mumkin
        serializer.save(author=self.request.user)

class MarkNotificationAsReadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        try:
            delivery = DeliveryLog.objects.get(pk=pk, user=request.user)
        except DeliveryLog.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        delivery.mark_read()
        return Response({"status": "ok"})

# ---------------- Admin Notification ----------------
class AdminSendNotificationView(APIView):
    permission_classes = (permissions.IsAdminUser,)  # faqat adminlar

    def post(self, request):
        """
        Admin notification yuboradi.
        Kutmoqda: {"text": "...", "recipients": [id1, id2], "data": {...}, "scheduled_at": "..."}
        """
        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save(author=request.user)

        # Har bir recipient uchun DeliveryLog yaratish
        for user in notification.recipients.all():
            DeliveryLog.objects.create(notification=notification, user=user)

        # TODO: Celery task orqali Firebase push yuborish
        return Response({"id": notification.id, "status": "created"}, status=status.HTTP_201_CREATED)
