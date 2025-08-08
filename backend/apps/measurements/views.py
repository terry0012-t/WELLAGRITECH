from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils.dateparse import parse_datetime
from django.db.models import Max
from apps.devices.models import Device
from .models import Measurement, Setting


# Create your views here.


class LatestMeasurementsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        device_id = request.query_params.get('device_id')
        if not device_id:
            return Response({"detail": "device_id requis"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            device = Device.objects.get(device_id=device_id, owner=request.user)
        except Device.DoesNotExist:
            return Response({"detail": "Device introuvable"}, status=status.HTTP_404_NOT_FOUND)
        measurement = device.measurements.order_by('-timestamp').values(
            'humidite_sol', 'niveau_eau', 'intrusion', 'etat_pompe', 'timestamp'
        ).first()
        return Response(measurement or {})


class MeasurementsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        device_id = request.query_params.get('device_id')
        from_dt = request.query_params.get('from')
        to_dt = request.query_params.get('to')
        limit = int(request.query_params.get('limit', '200'))
        if not device_id:
            return Response({"detail": "device_id requis"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            device = Device.objects.get(device_id=device_id, owner=request.user)
        except Device.DoesNotExist:
            return Response({"detail": "Device introuvable"}, status=status.HTTP_404_NOT_FOUND)
        qs = device.measurements.all()
        if from_dt:
            qs = qs.filter(timestamp__gte=parse_datetime(from_dt))
        if to_dt:
            qs = qs.filter(timestamp__lte=parse_datetime(to_dt))
        qs = qs.order_by('-timestamp')[:limit]
        data = list(qs.values('humidite_sol', 'niveau_eau', 'intrusion', 'etat_pompe', 'timestamp'))
        return Response(data)


class Esp32DataIngestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        device_id = request.data.get('device_id')
        device_key = request.headers.get('X-Device-Key')
        if not device_id or not device_key:
            return Response({"detail": "device_id et X-Device-Key requis"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            device = Device.objects.get(device_id=device_id, device_key=device_key)
        except Device.DoesNotExist:
            return Response({"detail": "Auth appareil invalide"}, status=status.HTTP_403_FORBIDDEN)
        payload = {
            'humidite_sol': request.data.get('humidite_sol'),
            'niveau_eau': request.data.get('niveau_eau'),
            'intrusion': request.data.get('intrusion', False),
            'etat_pompe': request.data.get('etat_pompe', False),
            'timestamp': request.data.get('timestamp'),
        }
        Measurement.objects.create(
            device=device,
            humidite_sol=payload['humidite_sol'],
            niveau_eau=payload['niveau_eau'],
            intrusion=payload['intrusion'],
            etat_pompe=payload['etat_pompe'],
            timestamp=parse_datetime(payload['timestamp']) if payload['timestamp'] else None,
        )
        device.last_seen = parse_datetime(payload['timestamp']) if payload['timestamp'] else None
        device.save(update_fields=['last_seen'])
        return Response({"status": "ok", "stored": True})


class SettingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        setting, _ = Setting.objects.get_or_create(user=request.user)
        data = {
            'humidite_seuil': setting.humidite_seuil,
            'irrigation_windows': setting.irrigation_windows,
            'notifications_enabled': setting.notifications_enabled,
        }
        return Response(data)

    def put(self, request):
        setting, _ = Setting.objects.get_or_create(user=request.user)
        setting.humidite_seuil = request.data.get('humidite_seuil', setting.humidite_seuil)
        setting.irrigation_windows = request.data.get('irrigation_windows', setting.irrigation_windows)
        setting.notifications_enabled = request.data.get('notifications_enabled', setting.notifications_enabled)
        setting.save()
        return Response({"status": "ok"})
