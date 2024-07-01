from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Doctor, Patient, Appointment

@csrf_exempt
def create_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        patient_id = request.POST.get('patient_id')
        appointment_date = parse_datetime(request.POST.get('appointment_date'))
        symptoms = request.POST.get('symptoms')

        try:
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                appointment_date=appointment_date,
                symptoms=symptoms
            )
            return JsonResponse({'status': 'success', 'appointment_id': appointment.id})
        except Doctor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Doctor not found'}, status=404)
        except Patient.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Patient not found'}, status=404)
        except Exception as e:
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
    if request.method == 'POST':
        appointment_date = parse_datetime(request.POST.get('appointment_date'))
        symptoms = request.POST.get('symptoms')
        prescription = request.POST.get('prescription')

        try:
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

# Create your views here.
