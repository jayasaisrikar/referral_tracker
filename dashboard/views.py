from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import ReferralEmployee, JobRole, Resume, ExtractedData
from .forms import ReferralEmployeeForm, JobRoleForm, ResumeUploadForm, SignUpForm
from django.core.files.storage import FileSystemStorage
from .utils import parse_resume_and_match_jobs

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def add_referral_employee(request):
    if request.method == 'POST':
        form = ReferralEmployeeForm(request.POST)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.user = request.user
            referral.save()
            messages.success(request, 'Referral employee added successfully.')
            return redirect('dashboard')
    else:
        form = ReferralEmployeeForm()
    return render(request, 'dashboard/referral_form.html', {'form': form})

@login_required
def add_job_role(request):
    if request.method == 'POST':
        form = JobRoleForm(request.POST)
        if form.is_valid():
            job_role = form.save(commit=False)
            job_role.user = request.user

            # Set default job_url if not provided by the user
            if not job_role.job_url:
                job_role.job_url = 'https://example.com/default-url'

            job_role.save()
            messages.success(request, 'Job role added successfully.')
            return redirect('dashboard')
    else:
        form = JobRoleForm()
    return render(request, 'dashboard/job_form.html', {'form': form})

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_instance = form.save(commit=False)
            resume_instance.user = request.user
            resume_instance.save()

            # Path to the uploaded resume
            resume_path = resume_instance.file.path

            # Retrieve all job roles from the database
            job_roles = JobRole.objects.all()

            # Parse the resume and match jobs
            matched_jobs, resume_text = parse_resume_and_match_jobs(resume_path, job_roles)

            # Save extracted data to the database
            extracted_data = ExtractedData(resume=resume_instance, content=resume_text)
            extracted_data.save()

            context = {
                'matched_jobs': matched_jobs,
                'resume_text': resume_text,
                'resume_instance': resume_instance,
            }

            return render(request, 'dashboard/matched_jobs.html', context)
    else:
        form = ResumeUploadForm()
    return render(request, 'dashboard/resume_upload.html', {'form': form})

@login_required
def search_referrals(request):
    job_roles = JobRole.objects.filter(user=request.user)
    referrals = ReferralEmployee.objects.filter(company_name__in=job_roles.values_list('company_name', flat=True))

    # Add job URLs to referrals
    for referral in referrals:
        matching_job = job_roles.filter(company_name=referral.company_name).first()
        if matching_job:
            referral.job_url = matching_job.job_url

    return render(request, 'dashboard/search_referrals.html', {'referrals': referrals})

@login_required
def analyze_resume(request):
    if request.method == 'POST':
        resume = Resume.objects.filter(user=request.user).latest('uploaded_at')
        job_roles = JobRole.objects.filter(user=request.user)
        job_roles_text = "\n".join([f"{job.company_name}: {job.role} - {job.job_description}" for job in job_roles])
        job_matches = parse_resume_and_match_jobs(resume.file.path, job_roles)
        return render(request, 'dashboard/job_matches.html', {'job_matches': job_matches})
    return redirect('dashboard')

@login_required
def view_job_roles(request):
    job_roles = JobRole.objects.filter(user=request.user)
    return render(request, 'dashboard/view_job_roles.html', {'job_roles': job_roles})

@login_required
def view_referrals(request):
    referrals = ReferralEmployee.objects.filter(user=request.user)
    return render(request, 'dashboard/view_referrals.html', {'referrals': referrals})

@login_required
def edit_job_role(request, job_role_id):
    job_role = get_object_or_404(JobRole, pk=job_role_id)
    if request.method == 'POST':
        form = JobRoleForm(request.POST, instance=job_role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job role updated successfully.')
            return redirect('view_job_roles')
    else:
        form = JobRoleForm(instance=job_role)
    return render(request, 'dashboard/edit_job_role.html', {'form': form})

@login_required
def edit_referral(request, referral_id):
    referral = get_object_or_404(ReferralEmployee, pk=referral_id)
    if request.method == 'POST':
        form = ReferralEmployeeForm(request.POST, instance=referral)
        if form.is_valid():
            form.save()
            messages.success(request, 'Referral updated successfully.')
            return redirect('view_referrals')
    else:
        form = ReferralEmployeeForm(instance=referral)
    return render(request, 'dashboard/edit_referral.html', {'form': form})

@login_required
def delete_job_role(request, job_role_id):
    job_role = get_object_or_404(JobRole, pk=job_role_id)

    if request.method == 'POST':
        job_role.delete()
        messages.success(request, 'Job role deleted successfully.')
        return redirect('view_job_roles')

    return redirect('view_job_roles')

@login_required
def delete_referral(request, referral_id):
    referral = get_object_or_404(ReferralEmployee, id=referral_id)

    if request.method == 'POST':
        referral.delete()
        messages.success(request, 'Referral deleted successfully.')

    return redirect('view_referrals')
