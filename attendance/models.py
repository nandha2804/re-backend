# attendance/models.py
from django.db import models
from django.contrib.auth import get_user_model

class InstituteLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField(default=50)  # Radius in meters to restrict QR code scan
    location_name = models.CharField(max_length=255)

    def __str__(self):
        return self.location_name

class LocationQRCode(models.Model):
    # Define fields for your model here
    location_name = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qrcodes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location_name


from user.models import Student  # Import the Student model from the user app

class Attendance(models.Model):
    student = models.ForeignKey(Student, related_name='attendance', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[('login', 'Login'), ('tea_break', 'Tea Break'), ('lunch', 'Lunch Break'), ('logout', 'Logout')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.name} - {self.type} at {self.timestamp}'



# User = get_user_model()

# class Attendance(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
#     type = models.CharField(max_length=20)
#     timestamp = models.DateTimeField()

#     def __str__(self):
#         return f"{self.student.username} - {self.type} - {self.timestamp}"
    
