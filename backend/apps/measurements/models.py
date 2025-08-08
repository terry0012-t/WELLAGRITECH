from django.db import models
from django.utils import timezone
from apps.devices.models import Device
from django.contrib.auth.models import User


class Measurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='measurements')
    humidite_sol = models.FloatField()
    niveau_eau = models.FloatField()
    intrusion = models.BooleanField(default=False)
    etat_pompe = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ('device', 'timestamp')


class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settings')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='settings', null=True, blank=True)
    humidite_seuil = models.FloatField(default=30.0)
    irrigation_windows = models.JSONField(default=list, blank=True)
    notifications_enabled = models.BooleanField(default=True)
