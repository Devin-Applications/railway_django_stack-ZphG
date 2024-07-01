from django.urls import path
from .views import create_appointment, list_appointments, update_appointment, delete_appointment

urlpatterns = [
    path('create/', create_appointment, name='create_appointment'),
    path('list/', list_appointments, name='list_appointments'),
    path('update/<int:appointment_id>/', update_appointment, name='update_appointment'),
    path('delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
]
