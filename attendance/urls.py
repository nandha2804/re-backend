# attendance/urls.py
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('generate_qr_code/', generate_qr_code, name='generate_qr_code'),
    path('mark-attendance/', views.mark_attendance, name='mark-attendance'),
    path('attendance/student/', views.get_student_attendance, name='student-attendance'),

]

