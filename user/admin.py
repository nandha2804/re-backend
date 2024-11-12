# user/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'user_type')  # Added 'user_type' to display

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)


