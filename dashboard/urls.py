# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('add-referral/', views.add_referral_employee, name='add_referral'),
    path('add-job-role/', views.add_job_role, name='add_job_role'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('search-referrals/', views.search_referrals, name='search_referrals'),
    path('analyze-resume/', views.analyze_resume, name='analyze_resume'),
    path('dashboard/view-job-roles/', views.view_job_roles, name='view_job_roles'),
    path('dashboard/view-referrals/', views.view_referrals, name='view_referrals'),
    path('edit-job-role/<int:job_role_id>/', views.edit_job_role, name='edit_job_role'),
    path('edit-referral/<int:referral_id>/', views.edit_referral, name='edit_referral'),
    path('delete-job-role/<int:job_role_id>/', views.delete_job_role, name='delete_job_role'),
    path('delete-referral/<int:referral_id>/', views.delete_referral, name='delete_referral'),
]