# reservations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Ruta: GET /api/reservations/count
    path('reservations/count', views.get_reservation_count, name='get_reservation_count'),

    # Ruta: POST /api/reservations/create
    path('reservations/create', views.create_reservation, name='create_reservation'),
]