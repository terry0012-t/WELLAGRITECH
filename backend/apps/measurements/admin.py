from django.contrib import admin
from .models import Measurement, Setting

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("device", "humidite_sol", "niveau_eau", "intrusion", "etat_pompe", "timestamp")
    list_filter = ("intrusion", "etat_pompe", "timestamp")

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("user", "device", "humidite_seuil", "notifications_enabled")
