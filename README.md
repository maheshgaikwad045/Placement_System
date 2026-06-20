<<<<<<< HEAD
# PlaceMe — Campus Placement Management System
### Built with Python 3.12 + Django 5.x

A full-featured, production-ready placement portal for companies, colleges, and students.

---

## Features

### Student Features
- Register & login with secure authentication
- Complete profile (college, CGPA, skills, degree, GitHub, LinkedIn)
- Browse & search jobs (by title, skill, location, type)
- Apply with resume upload + cover letter
- Track all applications with real-time status
- Withdraw applications
- View interview schedules

### Admin / Placement Cell Features
- Admin dashboard with stats overview
- Post, edit, and manage job listings
- Manage companies (add logo, details)
- View all student applications with filtering
- Update application status (Applied → Shortlisted → Interview → Selected/Rejected)
- Schedule interview date/time per student
- Internal HR notes per application
- View all registered students

---

## Project Structure

```
placement_system/
├── placement_system/      # Django project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── jobs/                  # Main app
│   ├── models.py          # Company, Job, Application, StudentProfile
│   ├── views.py           # All views (student + admin)
│   ├── forms.py           # All forms
│   ├── admin.py           # Django admin config
│   └── migrations/
├── templates/             # HTML templates
│   ├── base.html          # Base layout + navbar
│   ├── home.html          # Landing page
│   ├── dashboard.html     # Student dashboard
│   ├── accounts/          # Login, Register, Edit Profile
│   ├── jobs/              # Job List, Detail, Apply
│   └── admin/             # Admin panel templates
├── static/                # CSS/JS assets
├── media/                 # Uploaded files (resumes, logos)
├── db.sqlite3             # SQLite database
└── manage.py
```

---

## Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd placement_system
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install django pillow
```

### 2. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Run Development Server
```bash
python manage.py runserver
```
Open: http://127.0.0.1:8000

---

## Demo Credentials (after loading fixtures)

| Role    | Username  | Password   |
|---------|-----------|------------|
| Admin   | admin     | admin123   |
| Student | student1  | test1234!  |
| Student | student2  | test1234!  |

---

## Models

### Company
- `name`, `description`, `website`, `location`, `industry`, `logo`

### Job
- Linked to Company
- `title`, `description`, `requirements`, `job_type` (full-time/part-time/internship/contract)
- `salary_min/max`, `experience_years`, `skills_required`, `deadline`, `status`

### StudentProfile (extends User)
- `phone`, `college`, `degree`, `branch`, `graduation_year`, `cgpa`
- `skills`, `linkedin`, `github`, `bio`, `profile_picture`

### Application
- Links Student ↔ Job
- `status`: applied → shortlisted → interview → selected/rejected
- `cover_letter`, `resume`, `interview_date`, `notes` (HR internal)

---

## Technologies Used

| Tech | Purpose |
|------|---------|
| Python 3.12 | Backend language |
| Django 5.x | Web framework |
| SQLite | Database (use PostgreSQL for production) |
| Bootstrap 5 | Frontend UI |
| Font Awesome | Icons |
| Pillow | Image handling |

---

## Production Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Use environment variables for `SECRET_KEY`
- [ ] Switch to PostgreSQL: `pip install psycopg2-binary`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Run `python manage.py collectstatic`
- [ ] Use Gunicorn + Nginx for serving
- [ ] Add email backend for notifications
- [ ] Configure AWS S3 for media files

---

## Skills Demonstrated (for Placement)

✅ Django ORM & Models with relationships (ForeignKey, OneToOne)  
✅ User Authentication (login, logout, register, decorators)  
✅ File Uploads (resumes, profile pictures, logos)  
✅ CRUD Operations (Create, Read, Update, Delete)  
✅ Role-based Access Control (Student vs Staff)  
✅ Form Handling & Validation  
✅ Template Inheritance & Django Template Language  
✅ Search & Filter functionality (Q objects)  
✅ URL routing & named URLs  
✅ Django Admin customization  
✅ Bootstrap 5 responsive UI  
✅ MVC Architecture (Models-Views-Templates)  

---

*Built as a real-world placement project. Ready to extend with email notifications, PDF generation, and REST API.*

c:/Users/Admin/OneDrive/Desktop/Django/placement_system/.venv/Scripts/python.exe manage.py runserver
=======
# Placement_System
>>>>>>> 9232d7d3fe57d21c2c58f376857f8af376230135
