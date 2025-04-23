from django.db import models
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password
from django.templatetags.static import static
from .models import *
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # This automatically hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if 'dob' not in extra_fields:
            extra_fields['dob'] = '2000-01-01'

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    last_login = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.png')
    STUDENT = 'student'
    RECRUITER = 'recruiter'

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (RECRUITER, 'Recruiter'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,  # default role can be 'student'
    )
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    
    def get_profile_picture_url(self):
        # Return profile picture if uploaded, else return static default image
        if self.profile_picture:
            return self.profile_picture.url
        return static('profilepicture/default.png')
    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Reference to User model
    branch = models.CharField(max_length=100)
    year_of_graduation = models.IntegerField()

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    website = models.URLField()
    company_picture = models.ImageField(upload_to='company_pictures/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class CompanyRecruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Reference to User model
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

    

# Model for Placement Session
class PlacementSession(models.Model):
    session_name = models.CharField(max_length=150)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(CompanyRecruiter, on_delete=models.CASCADE)  # Linking recruiter
    date = models.DateField()
    student_selected = models.BigIntegerField(null=True, blank=True)
    session_end = models.DateTimeField()
    mode = models.CharField(max_length=255)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.session_name} - {self.company.name}"


class JobOpening(models.Model):
    company = models.ForeignKey(Company, related_name='job_openings', on_delete=models.CASCADE)
    session = models.ForeignKey(PlacementSession, related_name='job_openings', on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    skills =  models.CharField(max_length=200)
    posted_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.position} at {self.company.name}"


from django.db import models
from django.conf import settings
from placeapp.models import JobOpening

from django.db import models

from django.db import models
from django.core.exceptions import ValidationError

class JobApplication(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('Graduation', 'Graduation'),
        ('Master', 'Master'),
    ]

    GRADUATION_FIELDS = [
        ('BSc Computer Science', 'BSc Computer Science'),
        ('BSc IT', 'BSc IT'),
        ('BCom', 'BCom'),
        ('BBA', 'BBA'),
        ('BE Mechanical', 'BE Mechanical'),
        ('BE Electrical', 'BE Electrical'),
        ('BTech Civil', 'BTech Civil'),
        ('BTech CSE', 'BTech CSE'),
        ('BTech ECE', 'BTech ECE'),
        ('BTech Electronics', 'BTech Electronics'),
        ('Other', 'Other'),
    ]

    MASTER_FIELDS = [
        ('MSc Computer Science', 'MSc Computer Science'),
        ('MBA', 'MBA'),
        ('MCom', 'MCom'),
        ('ME Mechanical', 'ME Mechanical'),
        ('ME Electrical', 'ME Electrical'),
        ('MTech Civil', 'MTech Civil'),
        ('MTech Electronics', 'MTech Electronics'),
        ('MA Economics', 'MA Economics'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('contacted', 'Contacted'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey("JobOpening", on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="applications")
    name = models.CharField(max_length=100, help_text="Enter your full name.")
    email = models.EmailField(help_text="Enter a valid email address.")
    phone = models.CharField(max_length=15, help_text="Enter your phone number.")
    skills = models.TextField(help_text="List your skills separated by commas.")
    cover_letter = models.TextField(help_text="Write a detailed cover letter.")
    resume = models.FileField(upload_to='resumes/', help_text="Upload your resume.")
    location = models.CharField(max_length=100, help_text="Enter your current location.")
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, help_text="Select your education level.")
    field_of_study = models.CharField(max_length=50, help_text="Select your field of study.")
    certification = models.TextField(blank=True, null=True, help_text="List certifications (if any).")
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Enter your expected salary.")
    experience = models.TextField(blank=True, null=True, help_text="Describe your work experience (if any).")
    anything_else = models.TextField(blank=True, null=True, help_text="Add any additional information.")
    applied_on = models.DateTimeField(auto_now_add=True, help_text="Date and time of application submission.")

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', help_text="Current status of the application")  # ✅ NEW STATUS FIELD

    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_status_display()})"

    def clean(self):
        """
        Custom validation to ensure `field_of_study` matches the selected `education_level`.
        """
        valid_fields = self.GRADUATION_FIELDS if self.education_level == 'Graduation' else self.MASTER_FIELDS
        valid_field_names = [field[0] for field in valid_fields]

        if self.field_of_study not in valid_field_names:
            raise ValidationError(
                {"field_of_study": f"Invalid field of study for the selected education level: {self.education_level}"}
            )


from django.db import models

class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    contact_number = models.CharField(max_length=15, verbose_name="Contact Number")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted At")

    def __str__(self):
        return f"{self.name} ({self.email})"



class CompanyRegister(models.Model):
    company_name = models.CharField(max_length=150, verbose_name="Company Name")
    website = models.URLField(verbose_name="Company Website", blank=True, null=True)
    address = models.TextField(verbose_name="Company Address")
    recruiter_name = models.CharField(max_length=100, verbose_name="Recruiter's Name")
    recruiter_email = models.EmailField(verbose_name="Recruiter's Email")
    description = models.TextField(verbose_name="Company Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Registered At")

    def __str__(self):
        return self.company_name



