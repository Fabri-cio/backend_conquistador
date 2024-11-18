# mi_app/urls.py
from django.urls import path
from .views import forecast_view

urlpatterns = [
    path('api/forecast/', forecast_view, name='forecast'),
]
