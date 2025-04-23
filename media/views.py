from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout  # Import the logout function
from .forms import LoginForm, StudentSignupForm, RecruiterSignupForm
from .models import User, Student, Company, CompanyRecruiter, PlacementSession
import logging
from django.contrib.auth.decorators import login_required

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Homepage view
def homepage(request):
    return render(request, 'placeapp/home.html')

# Student list view
def student_list(request):
    students = Student.objects.all()
    return render(request, 'placeapp/student_list.html', {'students': students})

# Student detail view
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
        
        return render(request, 'placeapp/student_detail.html', {'student': student})
    except Student.DoesNotExist:
        return redirect('student_list')

# Company list view
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'placeapp/company_list.html', {'companies': companies})

# Company detail view
def company_detail(request, pk):
    try:
        company = Company.objects.get(pk=pk)
        return render(request, 'placeapp/company_details.html', {'company': company})
    except Company.DoesNotExist:
        return redirect('company_list')

# Placement session list view
from django.shortcuts import render
from .models import PlacementSession, JobOpening
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.http import HttpResponseForbidden
from placeapp.models import PlacementSession, CompanyRecruiter

from django.shortcuts import render
from placeapp.models import PlacementSession, CompanyRecruiter

from django.shortcuts import render
from .models import PlacementSession, CompanyRecruiter

def placement_session_list(request):
    user = request.user
    is_recruiter = CompanyRecruiter.objects.filter(user_id=user.id).exists()
    
    if is_recruiter:
        recruiter = CompanyRecruiter.objects.get(user_id=user.id)
        placement_sessions = PlacementSession.objects.filter(recruiter=recruiter)
    else:
        placement_sessions = PlacementSession.objects.all()

    return render(request, 'placeapp/session_list.html', {
        'placement_sessions': placement_sessions,
        'is_recruiter': is_recruiter,
        'session_count': placement_sessions.count(),  # Send session count to template
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import JobApplication

def update_application_status(request, application_id, status_type):
    """
    Update the application status (pending, shortlisted, contacted, rejected)
    """
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Adjust this as per your authentication flow

    # Get the application object
    application = get_object_or_404(JobApplication, id=application_id)

    # Handle status updates on form submission (POST request)
    if request.method == 'POST':
        # Valid status types
        valid_statuses = ['shortlisted', 'contacted', 'rejected']

        if status_type in valid_statuses:
            if status_type == 'shortlisted':
                application.status = 'shortlisted'
            elif status_type == 'contacted':
                if application.status == 'shortlisted':
                    application.status = 'contacted'
                else:
                    return render(request, 'placeapp/applications.html', {
                        'error': 'Application must be shortlisted first.',
                        'applications': JobApplication.objects.all()
                    })
            elif status_type == 'rejected':
                application.status = 'rejected'

            application.save()
            return redirect('applications')  # Replace 'applications' with your view name for displaying applications

    # Render the applications page if status is not updated
    applications = JobApplication.objects.all()
    return render(request, 'placeapp/applications.html', {'applications': applications})


# views.py

def create_job_opening(request, session_id):
    # Get the session based on ID
    session = PlacementSession.objects.get(id=session_id)
    print(session)
    # Only allow the recruiter linked to the session to create job openings
    if session.recruiter != request.user.companyrecruitor:
        return HttpResponseForbidden("You are not authorized to create jobs for this session.")

    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            job_opening = form.save(commit=False)
            job_opening.session = session  # Link the job to the session
            job_opening.save()
            return redirect('placement_session_detail', session_id=session.id)
    else:
        form = JobOpeningForm()

    return render(request, 'placeapp/create_job_opening.html', {'form': form, 'session': session})

# Placement session detail view
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from placeapp.models import PlacementSession, JobOpening, CompanyRecruiter

@login_required
def placement_session_detail(request, pk):
    # Retrieve the placement session
    session = get_object_or_404(PlacementSession, id=pk)
    
    # Retrieve job openings associated with the session
    job_openings = JobOpening.objects.filter(session=session)
    
    # Check if the user is a recruiter
    is_recruiter = CompanyRecruiter.objects.filter(user_id=request.user.id).exists()
    
    context = {
        'session': session,
        'job_openings': job_openings,
        'is_recruiter': is_recruiter,
    }
    
    return render(request, 'placeapp/placement_seassion_detail.html', context)

    
from django.shortcuts import render, redirect, get_object_or_404
from .models import PlacementSession, JobOpening, CompanyRecruiter
from .forms import PlacementSessionForm, JobOpeningForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.shortcuts import render, redirect, get_object_or_404
from .models import PlacementSession, CompanyRecruiter
@login_required
def create_placement_session(request):
    # Ensure the logged-in user is a recruiter
    try:
        recruiter = CompanyRecruiter.objects.get(user=request.user)
    except CompanyRecruiter.DoesNotExist:
        return redirect('error_page')  # Replace with an appropriate error page or message

    if request.method == "POST":
        form = PlacementSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.company = recruiter.company  # Set the company automatically based on the recruiter
            session.recruiter = recruiter  # Set the recruiter automatically
            session.save()
            return redirect('placement_session_list')  # Redirect to a success page
    else:
        form = PlacementSessionForm()

    return render(request, 'placeapp/create_placement_session.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from placeapp.forms import JobOpeningForm
from placeapp.models import PlacementSession, CompanyRecruiter, JobOpening

@login_required
def create_job_opening(request, session_id):
    # Get the current placement session
    placement_session = get_object_or_404(PlacementSession, id=session_id)
    
    # Ensure the logged-in user is a recruiter for the session
    try:
        recruiter = CompanyRecruiter.objects.get(user=request.user)
    except CompanyRecruiter.DoesNotExist:
        print("User is not a recruiter")
        return redirect('error_page')  # Redirect to an error page if the user is not a recruiter
    
    # Ensure the recruiter belongs to the company of this session
    if recruiter.company != placement_session.company:
        print("Company mismatch!")
        return redirect('error_page')  # Redirect if the company does not match

    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            # Save the form without committing to the database yet
            job_opening = form.save(commit=False)

            # Link the job opening to the session and the recruiter’s company
            job_opening.session = placement_session
            job_opening.company = recruiter.company

            job_opening.save()  # Save the job opening

            # Redirect after successful creation
            return redirect('placement_session_list')  # Adjust URL as needed
    else:
        form = JobOpeningForm()

    return render(request, 'placeapp/create_job_opening.html', {'form': form, 'placement_session': placement_session})



@login_required
def list_placement_sessions(request):
    recruiter = request.user.companyrecruiter  # Assuming the recruiter is logged in
    
    sessions = PlacementSession.objects.filter(recruiter=recruiter)  # Fetch sessions with job openings
    print(sessions)
    return render(request, 'placeapp/session_list.html', {'sessions': sessions})


@login_required
def view_jobs(request, session_id):
    # Get the session based on the session ID
    session = get_object_or_404(PlacementSession, id=session_id)

    # Get all the job openings associated with this session
    job_openings = JobOpening.objects.filter(session_id=session_id)

    # Check if the user is a recruiter
    is_recruiter = CompanyRecruiter.objects.filter(user=request.user).exists()

    return render(request, 'placeapp/view_jobs.html', {
        'session': session,
        'job_openings': job_openings,
        'is_recruiter': is_recruiter
    })


# Profile view (for the logged-in user)
def profile(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        return render(request, 'placeapp/profile.html', {'user': user})
    return redirect('login')

# Combined signup view for students and recruiters
from django.shortcuts import render, redirect
from .forms import StudentSignupForm, RecruiterSignupForm
from .models import User, Student, Company, CompanyRecruiter

from django.contrib.auth import login

def combined_signup_view(request):
    if request.method == 'POST':
        student_form = StudentSignupForm(request.POST)
        recruiter_form = RecruiterSignupForm(request.POST)

        if 'student_signup' in request.POST:
            if student_form.is_valid():
                # Save the user instance without committing to DB
                user = student_form.save(commit=False)
                user.role = User.STUDENT
                
                # Hash the password before saving the user
                user.set_password(user.password)  # This will hash the password
                user.save()  # Now the password will be saved in hashed form

                # Create a Student object and associate with user
                Student.objects.create(
                    user=user,
                    branch=student_form.cleaned_data['branch'],
                    year_of_graduation=student_form.cleaned_data['year_of_graduation']
                )
                login(request, user)  # Log the student in
                return redirect('login')

        elif 'recruiter_signup' in request.POST:
            if recruiter_form.is_valid():
                # Save the recruiter user instance without committing to DB
                user = recruiter_form.save(commit=False)
                user.role = User.RECRUITER  # Set role to 'recruiter'

                # Hash the password before saving the user
                user.set_password(user.password)  # Hash the password
                user.save()

                # Get the selected company from the form
                company = recruiter_form.cleaned_data['company']  # Get the company from the form

                # Create a CompanyRecruiter object and associate with user and the selected company
                CompanyRecruiter.objects.create(
                    user=user,
                    company=company,
                    position=recruiter_form.cleaned_data['position']
                )

                # Log the recruiter in after signing up
                login(request, user)
                return redirect('login')

    else:
        student_form = StudentSignupForm()
        recruiter_form = RecruiterSignupForm()

    return render(request, 'placeapp/combined_signup.html', {
        'student_form': student_form,
        'recruiter_form': recruiter_form
    })




# Login view for users
from django.contrib.auth.hashers import check_password

from .forms import LoginForm
from .models import User,JobOpening


from django.shortcuts import render, redirect
from .forms import LoginForm  # Assuming you have a custom LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm  # Your form with 'username' and 'password'

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:  # Authentication was successful
                login(request, user)  # Log the user in and set session
                print(f"Logged in as {user.username} with role {user.role}")  # Debugging log after login
                
                if user.role == User.STUDENT:
                    print("Logged in as Student")
                    return render(request, 'placeapp/home.html', {'user': user, 'stu': 'stu'})
                elif user.role == User.RECRUITER:
                    print("Logged in as Recruiter")
                    return render(request, 'placeapp/home.html', {'user': user})
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            print(form.errors)
    else:
        form = LoginForm()

    return render(request, 'placeapp/login.html', {'form': form})


def home_view(request):
    # Retrieve the user from the session
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    
    # Retrieve the role from the session
    role = request.session.get('role')

    # Pass both user and role to the template
    return render(request, 'placeapp/home.html', {'user': user, 'role': role})


# Logout view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to the home page after logout
from django.shortcuts import render

@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user
    return render(request, 'placeapp/profile.html', {'user': user})

def current_job_openings(request):
    # Logic to display current job openings for students
    jobs=JobOpening.objects.all()
    return render(request, 'placeapp/jobopening.html',{'jobs':jobs})

from django.contrib.auth.decorators import login_required

@login_required
def create_job(request, session_id):

    session = get_object_or_404(PlacementSession, id=session_id)

    try:
        recruiter = CompanyRecruiter.objects.get(user=request.user)
    except CompanyRecruiter.DoesNotExist:
        print("Recruiter does not exist for the logged-in user.")
        return redirect('error_page')

    if not recruiter.company:
        print("Recruiter has no associated company.")
        return redirect('error_page')

    if request.method == "POST":
        print("Form data received:", request.POST)
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.session = session
            job.company = recruiter.company
            try:
                job.save()
                print("Job created successfully.")
                return redirect('placement_sessions')
            except Exception as e:
                print(f"Error saving job: {e}")
        else:
            print("Form errors:", form.errors)
    else:
        form = JobOpeningForm()

    return render(request, 'placeapp/create_job.html', {'form': form, 'session': session})


def my_jobs(request):
    """View for students to see their job applications."""
    userid = request.user.id

    applications = JobApplication.objects.filter(user_id=userid).select_related('job__company')

    return render(request, 'placeapp/my_jobs.html', {'applications': applications})


from placeapp.models import JobOpening, JobApplication
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from placeapp.models import JobOpening, JobApplication
from placeapp.forms import JobApplicationForm

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)

    # Prevent recruiters from applying
    if request.user.role == 'Recruiter':
        return HttpResponseForbidden("Recruiters cannot apply for jobs.")

    # Check if the user has already applied
    if JobApplication.objects.filter(user_id=request.user.id, id=job_id).exists():
        messages.info(request, "You have already applied for this job.")
        return HttpResponseForbidden("You are already applied")

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            return redirect('placement_session_detail', pk=application.id)

    else:
        form = JobApplicationForm()

    return render(request, 'placeapp/apply_job.html', {'form': form, 'job': job})


from django.shortcuts import render, get_object_or_404
from placeapp.models import JobApplication

@login_required
def application_response(request, job_id):
    try:
        job = JobOpening.objects.get(pk=job_id)
        session_id = job.session.id if job.session else None
    except JobOpening.DoesNotExist:
        job = None
        session_id = None

    return render(request, 'placeapp/application_response.html', {
        'job': job,
        'session_id': session_id,
    })




@login_required
def view_applicants(request, job_id):
    # Ensure the user is a recruiter
    try:
        recruiter = CompanyRecruiter.objects.get(user_id=request.user.id)
    except CompanyRecruiter.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to view applicants.")

    # Get the job and ensure it belongs to a session associated with this recruiter
    job = get_object_or_404(JobOpening, id=job_id)
    print(job)
    
    # Get all applications for this job
    applications = JobApplication.objects.filter(job_id=job_id)
    

    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'placeapp/view_applicants.html', context)



from django.views.decorators.http import require_POST
from .models import JobApplication

@login_required
def toggle_shortlisted(request, application_id):
    """Toggle the shortlisted status of an application."""
    application = get_object_or_404(JobApplication, id=application_id)

    # Ensure the user is authorized to update
    if not request.user.is_staff:  # Modify the condition based on your user roles
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    application.shortlisted = not application.shortlisted
    application.save()

    return JsonResponse({'shortlisted': application.shortlisted})


@login_required
def toggle_contacted(request, application_id):
    """Toggle the contacted status of an application."""
    application = get_object_or_404(JobApplication, id=application_id)

    # Ensure the user is authorized to update
    if not request.user.is_staff:  # Modify the condition based on your user roles
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    application.contacted = not application.contacted
    application.save()

    return JsonResponse({'contacted': application.contacted})




from django.http import JsonResponse
from .models import JobOpening

def api_jobs(request, session_id):
    # Fetch job openings for the given session ID
    jobs = JobOpening.objects.filter(session_id=session_id).values(
        'position', 'description', 'location', 'qualification'
    )

    # Return jobs as a JSON response
    return JsonResponse({'jobs': list(jobs)})


from django.shortcuts import render, redirect
from .models import ContactUs, CompanyRegister

def contact_us(request):
    if request.method == 'POST':
        ContactUs.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            contact_number=request.POST['contact_number'],
            message=request.POST['message']
        )
        return redirect('home')  # Redirect to home page after submission
    return render(request, 'placeapp/contact_us.html')

def company_register(request):
    if request.method == 'POST':
        CompanyRegister.objects.create(
            company_name=request.POST['company_name'],
            website=request.POST.get('website', ''),
            address=request.POST['address'],
            recruiter_name=request.POST['recruiter_name'],
            recruiter_email=request.POST['recruiter_email'],
            description=request.POST.get('description', '')
        )
        return redirect('home')  # Redirect to home page after submission
    return render(request, 'placeapp/company_register.html')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import JobApplication

@require_POST
@csrf_protect
def toggle_contacted(request, application_id):
    try:
        application = get_object_or_404(JobApplication, id=application_id)
        application.contacted = not application.contacted
        application.save()
        return JsonResponse({
            "success": True,
            "contacted": application.contacted,
            "message": "Status updated successfully"
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import JobApplication
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import JobApplication
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@csrf_exempt
def toggle_contacted(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication, id=application_id)
        application.contacted = not application.contacted
        application.save()
        return JsonResponse({"success": True, "contacted": application.contacted})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def toggle_shortlisted(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication, id=application_id)
        application.shortlisted = not application.shortlisted
        application.save()
        return JsonResponse({"success": True, "shortlisted": application.shortlisted})
    return JsonResponse({"error": "Invalid request method"}, status=400)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import JobApplication

@login_required
def view_applications(request):
    applications = JobApplication.objects.filter(user=request.user).select_related('job')
    return render(request, 'placeapp/view_applications.html', {'applications': applications})



from django.http import JsonResponse
from django.utils.timezone import now
from .models import JobOpening, JobApplication

def check_application_status(request, job_id):
    """Check if the user has already applied and if the job session is expired."""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 403, 'message': 'User not authenticated'})

    try:
        job = JobOpening.objects.get(id=job_id)
        
        # Check if session is expired
        if job.session.session_end < now():
            return JsonResponse({'status': 400, 'message': 'This job session has expired.'})

        # Check if user already applied
        if JobApplication.objects.filter(user=request.user, job=job).exists():
            return JsonResponse({'status': 400, 'message': 'You have already applied for this job.'})

        # If everything is valid
        return JsonResponse({'status': 200, 'message': 'Application allowed.'})
    
    except JobOpening.DoesNotExist:
        return JsonResponse({'status': 404, 'message': 'Job not found.'})
