from django.urls import path
from . import views

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Homepage and student/company placement-related views
    path('', views.homepage, name='homepage'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('companies/', views.company_list, name='company_list'),
    path('companies/<int:pk>/', views.company_detail, name='company_detail'),
    # path('placements/', views.placement_session_list, name='placement_session_list'),
    path('placements/<int:pk>/', views.placement_session_detail, name='placement_session_detail'),  # Placement session detail page
    path('my-applications/', views.view_applications, name='view_applications'),
    path('check-application/<int:pk>/', views.check_application_status, name='check_application_status'),
    path('my-applications/', views.my_jobs, name='my_jobs'),
    # Login, signup, profile, and logout views
    path('signup/', views.combined_signup_view, name='combined_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),# Change the URL pattern to accept the student ID as a parameter
    path('student/profile/<int:pk>/', views.student_detail, name='student_profile'),

    path('current_job_openings/', views.current_job_openings, name='current_job_openings'),
    path('create-session/',  views.create_placement_session, name='create_session'),
    path('create-job/<int:session_id>/',  views.create_job, name='create_job_opening'),
    path('placement-sessions/', views.placement_session_list, name='placement_session_list'),
    path('placement-session/<int:session_id>/create-job/', views.create_job_opening, name='create_job_opening'),
    path('placement-session/<int:session_id>/view-jobs/', views.view_jobs, name='view_jobs'),
    
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('application/<int:job_id>/response/', views.application_response, name='application_response'),
    path('application/<int:application_id>/toggle-shortlisted/', views.toggle_shortlisted, name='toggle_shortlisted'),
    path('application/<int:application_id>/toggle-contacted/', views.toggle_contacted, name='toggle_contacted'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('company-register/', views.company_register, name='company_register'),
    path('application/<int:application_id>/toggle-contacted/', views.toggle_contacted, name='toggle_contacted'),
    path('application/<int:application_id>/toggle-shortlisted/', views.toggle_shortlisted, name='toggle_shortlisted'),
    
    
path('application/<int:application_id>/update-status/<str:status_type>/', views.update_application_status, name='update_application_status'),]