# Generated by Django 5.1.3 on 2024-11-10 11:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
        ('user', '0002_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationQRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=255)),
                ('qr_code', models.ImageField(upload_to='qrcodes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='user.student'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='type',
            field=models.CharField(choices=[('login', 'Login'), ('tea_break', 'Tea Break'), ('lunch', 'Lunch Break'), ('logout', 'Logout')], max_length=20),
        ),
    ]
