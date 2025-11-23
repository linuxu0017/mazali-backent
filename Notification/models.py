from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    author = models.ForeignKey(User, related_name="authored_notifications", on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    recipients = models.ManyToManyField(User, related_name="notifications")
    data = models.JSONField(blank=True, null=True)
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification {self.id} by {self.author}"

class Device(models.Model):
    PLATFORM_CHOICES = (("android", "Android"), ("ios", "iOS"))
    user = models.ForeignKey(User, related_name="devices", on_delete=models.CASCADE)
    registration_id = models.CharField(max_length=512, unique=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.platform} - {self.registration_id[:20]}"

class DeliveryLog(models.Model):
    notification = models.ForeignKey(Notification, related_name="deliveries", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="notification_deliveries", on_delete=models.CASCADE)
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.SET_NULL)
    delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    response = models.JSONField(null=True, blank=True)

    def mark_delivered(self, response=None):
        self.delivered = True
        self.delivered_at = timezone.now()
        if response is not None:
            self.response = response
        self.save()

    def mark_read(self):
        self.read = True
        self.read_at = timezone.now()
        self.save()

    class Meta:
        indexes = [models.Index(fields=["user", "delivered"])]
