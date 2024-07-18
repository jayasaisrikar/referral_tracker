# dashboard/forms.py

from django import forms
from .models import ReferralEmployee, JobRole, Resume
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ReferralEmployeeForm(forms.ModelForm):
    class Meta:
        model = ReferralEmployee
        fields = ['company_name', 'employee_name', 'linkedin_url']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'employee_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }

class JobRoleForm(forms.ModelForm):
    class Meta:
        model = JobRole
        fields = ['company_name', 'role', 'job_description', 'job_id', 'job_url']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'role': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'job_description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 4}),
            'job_id': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'job_url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }
