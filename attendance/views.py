# attendance/views.py
from django.http import JsonResponse
from .models import InstituteLocation
from django.views.decorators.csrf import csrf_exempt
import json
from qrcode import make
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid
import os
import pyqrcode 
import png 
from pyqrcode import QRCode 
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework import status
from .models import LocationQRCode



# Ensure a default location exists
def set_default_location():
    if not InstituteLocation.objects.exists():
        default_location = InstituteLocation.objects.create(
            location_name="Institute Default Location",
            latitude=12.9237931,
            longitude=77.6063159,
            radius=50
        )
        print(f"Default location set: {default_location}")

set_default_location()

@csrf_exempt
def generate_qr_code(request):
    if request.method == 'POST':
        try:
            # Preconfigured default location and link
            location = "Institute Default Location"
            latitude = 12.910788
            longitude = 77.5998971
            link = "/attendance"

            # QR code data
            qr_data = json.dumps({
                "location": location, 
                "latitude": latitude, 
                "longitude": longitude, 
                "link": link
            })

#Generate the QR code using pyqrcode and save as PNG
            qr = pyqrcode.create(qr_data)
            
            # Define file paths and names
            qr_code_name = f"qr.png"
            qr_code_path = os.path.join("qr_codes", qr_code_name)
            qr_code_full_path = os.path.join(settings.MEDIA_ROOT, qr_code_path)

            # Save the QR code as PNG
            with open(qr_code_full_path, 'wb') as f:
                qr.png(f, scale=6)

            # URL for accessing the QR code
            qr_code_url = f"http://localhost:8000/media/{qr_code_path}"

            return JsonResponse({'success': True, 'qrCodeUrl': qr_code_url})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


User = get_user_model()

@api_view(['GET'])
def get_student_attendance(request, student_id):
    student = get_object_or_404(User, id=student_id)
    attendance_records = Attendance.objects.filter(student=student)
    serializer = AttendanceSerializer(attendance_records, many=True)
    return Response({
        'student': {
            'id': student.id,
            'name': student.username,
        },
        'attendance': serializer.data
    })

@api_view(['POST'])
def mark_attendance(request):
    student = request.user  # Assuming the user is authenticated
    data = request.data
    attendance_type = data.get('type')
    timestamp = data.get('timestamp', timezone.now())

    Attendance.objects.create(
        student=student,
        type=attendance_type,
        timestamp=timestamp
    )
    return Response({'message': 'Attendance marked successfully'}, status=status.HTTP_201_CREATED)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance
from .serializers import AttendanceSerializer

class StudentAttendanceView(APIView):
    def get(self, request, student_id, *args, **kwargs):
        # Fetch the attendance for the given student ID
        try:
            attendance = Attendance.objects.filter(student_id=student_id)
            serializer = AttendanceSerializer(attendance, many=True)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            return Response({"detail": "Attendance not found."}, status=status.HTTP_404_NOT_FOUND)





# from django.http import JsonResponse
# from .models import InstituteLocation, Attendance
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# import uuid
# import os
# import pyqrcode
# from django.utils import timezone
# from django.conf import settings


# # Ensure a default location exists
# def set_default_location():
#     if not InstituteLocation.objects.exists():
#         default_location = InstituteLocation.objects.create(
#             location_name="Institute Default Location",
#             latitude=12.918234,
#             longitude=77.605315,
#             radius=50
#         )
#         print(f"Default location set: {default_location}")

# set_default_location()

# @csrf_exempt
# def generate_qr_code(request):
#     if request.method == 'POST':
#         try:
#             # Preconfigured default location and link
#             location = "Institute Default Location"
#             latitude = 12.918234
#             longitude = 77.605315
#             link = "/attendance"

#             # QR code data
#             qr_data = json.dumps({
#                 "location": location, 
#                 "latitude": latitude, 
#                 "longitude": longitude, 
#                 "link": link
#             })

#             # Directory where QR codes are stored
#             qr_code_directory = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
            
#             # Delete old QR code files
#             if os.path.exists(qr_code_directory):
#                 for filename in os.listdir(qr_code_directory):
#                     file_path = os.path.join(qr_code_directory, filename)
#                     if os.path.isfile(file_path):
#                         os.remove(file_path)
            
#             # Generate the QR code using pyqrcode and save as PNG
#             qr = pyqrcode.create(qr_data)
            
#             # Define file paths and names
#             qr_code_name = f"{uuid.uuid4()}.png"
#             qr_code_path = os.path.join("qr_codes", qr_code_name)
#             qr_code_full_path = os.path.join(settings.MEDIA_ROOT, qr_code_path)

#             # Save the QR code as PNG
#             with open(qr_code_full_path, 'wb') as f:
#                 qr.png(f, scale=6)

#             # URL for accessing the QR code
#             qr_code_url = f"http://localhost:8000/media/{qr_code_path}"

#             return JsonResponse({'success': True, 'qrCodeUrl': qr_code_url})
        
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# @csrf_exempt
# def mark_attendance(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             attendance_type = data.get('type')
#             timestamp = data.get('timestamp', timezone.now().isoformat())

#             # Save to the database
#             Attendance.objects.create(type=attendance_type, timestamp=timestamp)

#             return JsonResponse({'message': 'Attendance marked successfully'}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)
