from django.urls import path
from .views import DeviceListView, DeviceCommandView

urlpatterns = [
    path('', DeviceListView.as_view(), name='devices_list'),
    path('<uuid:pk>/command/', DeviceCommandView.as_view(), name='device_command'),
]