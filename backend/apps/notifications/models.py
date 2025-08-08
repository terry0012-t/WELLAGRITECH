from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    TYPE_CHOICES = (
        ('tank_empty', 'Tank Empty'),
        ('soil_dry', 'Soil Dry'),
        ('intrusion_detected', 'Intrusion Detected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    payload = models.JSONField(default=dict, blank=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
