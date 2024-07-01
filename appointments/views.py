from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Doctor, Patient, Appointment
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def create_appointment(request):
    logger.info(f"Received request at {request.path}")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Request data: {data}")
            doctor_id = data.get('doctor')
            patient_id = data.get('patient')
            appointment_date = parse_datetime(data.get('scheduled_time'))
            symptoms = data.get('symptoms')

            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                appointment_date=appointment_date,
                symptoms=symptoms
            )
            logger.info(f"Appointment created with ID: {appointment.id}")
            return JsonResponse({'status': 'success', 'appointment_id': appointment.id})
        except Doctor.DoesNotExist:
            logger.error("Doctor not found")
            return JsonResponse({'status': 'error', 'message': 'Doctor not found'}, status=404)
        except Patient.DoesNotExist:
            logger.error("Patient not found")
            return JsonResponse({'status': 'error', 'message': 'Patient not found'}, status=404)
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def list_appointments(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        appointments_list = [
            {
                'id': appointment.id,
                'doctor': appointment.doctor.user.username,
                'patient': appointment.patient.user.username,
                'appointment_date': appointment.appointment_date,
                'symptoms': appointment.symptoms,
                'prescription': appointment.prescription
            }
            for appointment in appointments
        ]
        return JsonResponse({'status': 'success', 'appointments': appointments_list})

@csrf_exempt
def update_appointment(request, appointment_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            appointment_date_str = data.get('appointment_date')
            appointment_date = parse_datetime(appointment_date_str) if appointment_date_str else None
            symptoms = data.get('symptoms')
            prescription = data.get('prescription')

            appointment = Appointment.objects.get(id=appointment_id)
            if appointment_date:
                appointment.appointment_date = appointment_date
            if symptoms:
                appointment.symptoms = symptoms
            if prescription:
                appointment.prescription = prescription
            appointment.save()
            return JsonResponse({'status': 'success', 'message': 'Appointment updated successfully'})
        except Appointment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Appointment not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def delete_appointment(request, appointment_id):
    if request.method == 'DELETE':
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            return JsonResponse({'status': 'success', 'message': 'Appointment deleted successfully'})
        except Appointment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Appointment not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
