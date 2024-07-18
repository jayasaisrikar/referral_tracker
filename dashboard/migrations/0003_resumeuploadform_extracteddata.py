# Generated by Django 5.0.4 on 2024-07-07 16:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_jobrole_job_url_alter_jobrole_job_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeUploadForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(upload_to='resumes/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExtractedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('extracted_at', models.DateTimeField(auto_now_add=True)),
                ('resume', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.resume')),
            ],
        ),
    ]