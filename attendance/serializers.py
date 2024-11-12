# attendance/serializers.py
from rest_framework import serializers
from .models import LocationQRCode, InstituteLocation
from .models import Attendance

class InstituteLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteLocation
        fields = ['id', 'latitude', 'longitude', 'radius', 'location_name']

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationQRCode
        fields = ['location', 'qr_code_image', 'created_at']



class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['type', 'timestamp']









