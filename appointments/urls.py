from django.urls import path
from .views import create_appointment, list_appointments

urlpatterns = [
    path('create/', create_appointment, name='create_appointment'),
    path('list/', list_appointments, name='list_appointments'),
]
