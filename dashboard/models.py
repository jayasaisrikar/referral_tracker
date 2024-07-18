# models.py
from django.db import models
from django.contrib.auth.models import User

class ReferralEmployee(models.Model):
    company_name = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=100)
    linkedin_url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class JobRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    job_description = models.TextField()
    job_id = models.CharField(max_length=50)
    job_url = models.URLField(max_length=200)  # Add this line

    def __str__(self):
        return f"{self.company_name} - {self.role}"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExtractedData(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    content = models.TextField()
    extracted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:50]

class ResumeUploadForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume uploaded by {self.user.username} at {self.uploaded_at}"