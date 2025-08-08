import uuid
from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=120, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    last_seen = models.DateTimeField(null=True, blank=True)
    firmware_version = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    device_key = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.device_id}"


class Command(models.Model):
    COMMAND_TYPES = (
        ('pump_on', 'Pump On'),
        ('pump_off', 'Pump Off'),
        ('reboot', 'Reboot'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('failed', 'Failed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='commands')
    command_type = models.CharField(max_length=20, choices=COMMAND_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.device.device_id}:{self.command_type}:{self.status}"
