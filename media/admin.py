from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Company, CompanyRecruiter, PlacementSession, JobOpening, JobApplication, ContactUs, CompanyRegister

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone', 'role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_active', 'is_staff', 'role')
    fieldsets = (
        ('Personal Info', {'fields': ('name', 'username', 'email', 'phone', 'dob', 'profile_picture', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Security', {'fields': ('password',)}),
    )
    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('name', 'username', 'email', 'password1', 'password2', 'phone', 'dob', 'role', 'is_staff', 'is_superuser'),
        }),
    )
    ordering = ('username',)

# Student Admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'year_of_graduation')
    search_fields = ('user__username', 'branch', 'year_of_graduation')

# Company Admin
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_email', 'contact_phone')
    search_fields = ('name', 'location', 'contact_email')
    list_filter = ('location',)

# Company Recruiter Admin
class CompanyRecruiterAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position')
    search_fields = ('user__username', 'company__name', 'position')

# Placement Session Admin
class PlacementSessionAdmin(admin.ModelAdmin):
    list_display = ('session_name', 'company', 'recruiter', 'date', 'session_end', 'location', 'mode', 'student_selected')
    search_fields = ('session_name', 'company__name', 'recruiter__user__username')
    list_filter = ('date', 'location', 'mode')

# Job Opening Admin
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'session', 'location', 'qualification', 'skills', 'posted_on')
    search_fields = ('position', 'company__name', 'location', 'skills')
    list_filter = ('posted_on', 'location', 'qualification')

# ✅ FIXED: Job Application Admin (Now using `status` instead of `shortlisted/contacted`)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job', 'education_level', 'status', 'applied_on')  # Replaced 'shortlisted' & 'contacted' with 'status'
    search_fields = ('name', 'email', 'job__position', 'education_level')
    list_filter = ('education_level', 'status', 'applied_on')  # Now filtering by `status`

# Contact Us Admin
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_number', 'created_at')
    search_fields = ('name', 'email', 'contact_number')
    list_filter = ('created_at',)

# Company Register Admin
class CompanyRegisterAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'recruiter_name', 'recruiter_email', 'website', 'created_at')
    search_fields = ('company_name', 'recruiter_name', 'recruiter_email')
    list_filter = ('created_at',)

# Register all models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyRecruiter, CompanyRecruiterAdmin)
admin.site.register(PlacementSession, PlacementSessionAdmin)
admin.site.register(JobOpening, JobOpeningAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)  # ✅ Fixed
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(CompanyRegister, CompanyRegisterAdmin)
