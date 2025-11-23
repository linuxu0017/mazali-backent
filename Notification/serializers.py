from rest_framework import serializers
from .models import Notification, DeliveryLog, Device
from django.contrib.auth import get_user_model

User = get_user_model()  # Bu endi haqiqiy model klassini qaytaradi

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("id", "registration_id", "platform", "active")

class NotificationSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    recipients = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Notification
        fields = ("id", "author", "text", "recipients", "data", "sent", "created_at", "scheduled_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamic queryset for recipients based on User model
        self.fields['recipients'].queryset = self.Meta.model._meta.get_field('recipients').related_model.objects.all()

    def create(self, validated_data):
        recipients = validated_data.pop('recipients', [])
        notification = Notification.objects.create(**validated_data)
        notification.recipients.set(recipients)
        return notification

class DeliveryLogSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = DeliveryLog
        fields = ("id", "notification", "delivered", "delivered_at", "read", "read_at", "response")
