from django.urls import path
from .views import LatestMeasurementsView, MeasurementsListView, Esp32DataIngestView, SettingsView

urlpatterns = [
    path('latest/', LatestMeasurementsView.as_view(), name='latest_measurements'),
    path('', MeasurementsListView.as_view(), name='measurements_list'),
    path('esp32/data/', Esp32DataIngestView.as_view(), name='esp32_data_ingest'),
    path('settings/', SettingsView.as_view(), name='user_settings'),
]