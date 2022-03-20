from django.urls import path

from measurement.views import SensorView, SingleSensorView, MeasurementView, SingleMeasurementView

urlpatterns = [
    path('sensors/', SensorView.as_view()),
    path('sensors/<pk>/', SingleSensorView.as_view()),
    path('measurements/', MeasurementView.as_view()),
    path('measurements/<pk>/', SingleMeasurementView.as_view()),
]
