from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from jobs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('applications/<int:pk>/withdraw/', views.withdraw_application, name='withdraw_application'),
    # Staff/Admin URLs
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/jobs/', views.manage_jobs, name='manage_jobs'),
    path('admin-panel/jobs/add/', views.add_job, name='add_job'),
    path('admin-panel/jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('admin-panel/applications/', views.manage_applications, name='manage_applications'),
    path('admin-panel/applications/<int:pk>/update/', views.update_application_status, name='update_application_status'),
    path('admin-panel/companies/', views.manage_companies, name='manage_companies'),
    path('admin-panel/companies/add/', views.add_company, name='add_company'),
    path('admin-panel/students/', views.student_list, name='student_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
