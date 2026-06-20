from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import Job, Company, Application, StudentProfile
from .forms import (StudentRegistrationForm, StudentProfileForm,
                    JobApplicationForm, JobForm, ApplicationStatusForm, CompanyForm)


def home(request):
    latest_jobs = Job.objects.filter(status='active').select_related('company')[:6]
    companies = Company.objects.annotate(job_count=Count('jobs')).order_by('-job_count')[:4]
    total_jobs = Job.objects.filter(status='active').count()
    total_companies = Company.objects.count()
    total_placed = Application.objects.filter(status='selected').count()
    return render(request, 'home.html', {
        'latest_jobs': latest_jobs,
        'companies': companies,
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'total_placed': total_placed,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Complete your profile to get started.')
            return redirect('edit_profile')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    try:
        profile = request.user.profile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)

    applications = Application.objects.filter(applicant=request.user).select_related('job', 'job__company')
    active_jobs = Job.objects.filter(status='active').count()
    return render(request, 'dashboard.html', {
        'profile': profile,
        'applications': applications,
        'active_jobs': active_jobs,
        'stats': {
            'applied': applications.filter(status='applied').count(),
            'shortlisted': applications.filter(status='shortlisted').count(),
            'interview': applications.filter(status='interview').count(),
            'selected': applications.filter(status='selected').count(),
        }
    })


@login_required
def edit_profile(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


def job_list(request):
    jobs = Job.objects.filter(status='active').select_related('company')
    query = request.GET.get('q', '')
    job_type = request.GET.get('type', '')
    location = request.GET.get('location', '')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__name__icontains=query) |
            Q(skills_required__icontains=query)
        )
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'query': query,
        'job_type': job_type,
        'location': location,
        'job_types': Job.JOB_TYPE_CHOICES,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    related_jobs = Job.objects.filter(company=job.company, status='active').exclude(pk=pk)[:3]
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied,
        'related_jobs': related_jobs,
    })


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, status='active')
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, f'Successfully applied for {job.title}!')
            return redirect('dashboard')
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@login_required
def withdraw_application(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    application.status = 'withdrawn'
    application.save()
    messages.success(request, 'Application withdrawn.')
    return redirect('dashboard')


# --- Admin / Staff Views ---

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    total_students = StudentProfile.objects.count()
    total_applications = Application.objects.count()
    total_companies = Company.objects.count()
    active_jobs = Job.objects.filter(status='active').count()
    recent_apps = Application.objects.select_related('job', 'applicant', 'job__company').order_by('-applied_at')[:10]
    status_counts = {
        'applied': Application.objects.filter(status='applied').count(),
        'shortlisted': Application.objects.filter(status='shortlisted').count(),
        'interview': Application.objects.filter(status='interview').count(),
        'selected': Application.objects.filter(status='selected').count(),
        'rejected': Application.objects.filter(status='rejected').count(),
    }
    return render(request, 'admin/dashboard.html', {
        'total_students': total_students,
        'total_applications': total_applications,
        'total_companies': total_companies,
        'active_jobs': active_jobs,
        'recent_apps': recent_apps,
        'status_counts': status_counts,
    })


@login_required
def manage_jobs(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    jobs = Job.objects.select_related('company').annotate(app_count=Count('applications'))
    return render(request, 'admin/manage_jobs.html', {'jobs': jobs})


@login_required
def add_job(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('manage_jobs')
    else:
        form = JobForm()
    return render(request, 'admin/job_form.html', {'form': form, 'title': 'Post New Job'})


@login_required
def edit_job(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('manage_jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'admin/job_form.html', {'form': form, 'title': 'Edit Job', 'job': job})


@login_required
def manage_applications(request, job_pk=None):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    applications = Application.objects.select_related('job', 'applicant', 'job__company', 'applicant__profile')
    if job_pk:
        applications = applications.filter(job_id=job_pk)
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    return render(request, 'admin/manage_applications.html', {
        'applications': applications,
        'statuses': Application.STATUS_CHOICES,
        'status_filter': status_filter,
    })


@login_required
def update_application_status(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}')
            return redirect('manage_applications')
    else:
        form = ApplicationStatusForm(instance=application)
    return render(request, 'admin/update_status.html', {'form': form, 'application': application})


@login_required
def manage_companies(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    companies = Company.objects.annotate(job_count=Count('jobs'))
    return render(request, 'admin/manage_companies.html', {'companies': companies})


@login_required
def add_company(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company added successfully!')
            return redirect('manage_companies')
    else:
        form = CompanyForm()
    return render(request, 'admin/company_form.html', {'form': form})


@login_required
def student_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    profiles = StudentProfile.objects.select_related('user').annotate(
        app_count=Count('user__applications')
    )
    return render(request, 'admin/student_list.html', {'profiles': profiles})
