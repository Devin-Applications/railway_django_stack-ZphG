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

# Create your views here.
