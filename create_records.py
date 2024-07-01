import os
import django
from django.contrib.auth.models import User
from appointments.models import Doctor, Patient

os.environ['DJANGO_SETTINGS_MODULE'] = 'railway_django_stack.settings'
django.setup()

# Create a user for the doctor
doctor_user = User.objects.create_user(username='drsmith', password='password123')
doctor_user.save()

# Create a doctor record
doctor = Doctor.objects.create(
    user=doctor_user,
    specialization='Cardiology',
    phone_number='1234567890',
    address='123 Heart St, Health City'
)
doctor.save()

# Create a user for the patient
patient_user = User.objects.create_user(username='john_doe', password='password123')
patient_user.save()

# Create a patient record
patient = Patient.objects.create(
    user=patient_user,
    phone_number='0987654321',
    address='456 Wellness Ave, Health City'
)
patient.save()

print(f"Doctor ID: {doctor.id}, Patient ID: {patient.id}")
