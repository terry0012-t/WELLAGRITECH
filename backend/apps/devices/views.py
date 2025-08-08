from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Device, Command
from rest_framework.views import APIView


# Create your views here.


class DeviceListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        devices = self.get_queryset().values(
            'id', 'device_id', 'name', 'last_seen', 'firmware_version', 'is_active'
        )
        return Response(list(devices))


class DeviceCommandView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        command = request.data.get('command')
        try:
            device = Device.objects.get(pk=pk, owner=request.user)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        if command not in ['pump_on', 'pump_off', 'reboot']:
            return Response({"detail": "Invalid command"}, status=status.HTTP_400_BAD_REQUEST)
        cmd = Command.objects.create(device=device, command_type=command)
        return Response({"status": "queued", "command_id": str(cmd.id)}, status=status.HTTP_202_ACCEPTED)
