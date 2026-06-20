from django.contrib import admin
from .models import Company, Job, Application, StudentProfile

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'location', 'website']
    search_fields = ['name', 'industry']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'job_type']
    search_fields = ['title', 'company__name']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['applicant__username', 'job__title']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'college', 'degree', 'graduation_year', 'cgpa']
    search_fields = ['user__username', 'user__first_name', 'college']
