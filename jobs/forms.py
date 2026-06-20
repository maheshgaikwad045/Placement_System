from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Application, StudentProfile, Job, Company


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.TextInput(attrs={'placeholder': 'Python, Django, SQL, ...'}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write a compelling cover letter...'}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['posted_by', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'skills_required': forms.TextInput(attrs={'placeholder': 'Python, Django, REST API, ...'}),
        }


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'interview_date', 'notes']
        widgets = {
            'interview_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
