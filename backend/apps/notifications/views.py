from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Notification
from rest_framework.response import Response

# Create your views here.


class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset().values('id', 'type', 'payload', 'seen', 'created_at')
        return Response(list(qs))
