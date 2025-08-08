from django.contrib import admin
from .models import Device, Command

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("device_id", "owner", "is_active", "last_seen")
    search_fields = ("device_id", "owner__username")

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ("device", "command_type", "status", "created_at")
    list_filter = ("command_type", "status")
