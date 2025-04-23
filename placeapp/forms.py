from django import forms
from .models import User, Student, CompanyRecruiter

class StudentSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    branch = forms.CharField(max_length=100)
    year_of_graduation = forms.IntegerField()

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'phone', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        print(f"Student Form - Password: {password}, Confirm Password: {confirm_password}")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


from django import forms
from .models import User, Company

class RecruiterSignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label="Password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Confirm Password",
    )
    position = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your Position'}),
        label="Position",
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=True,
        label="Company",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the company you represent."
    )

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'phone', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'name': "Full Name",
            'username': "Username",
            'email': "Email Address",
            'phone': "Phone Number",
            'dob': "Date of Birth",
        }
        help_texts = {
            'email': "We'll never share your email with anyone else.",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data



    
from django import forms
from .models import User  # Make sure to import the User model

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)





from django import forms
from .models import PlacementSession, JobOpening

class PlacementSessionForm(forms.ModelForm):
    class Meta:
        model = PlacementSession
        fields = ['session_name', 'date', 'session_end', 'mode', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'session_end': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from placeapp.models import JobOpening

class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['position', 'description', 'location', 'qualification', 'skills']



from django import forms
from placeapp.models import JobApplication

from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'name', 'email', 'phone', 'skills', 'cover_letter', 'resume', 
            'location', 'education_level', 'field_of_study', 'certification', 
            'expected_salary', 'experience', 'anything_else'
        ]
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'education_level': forms.Select(attrs={'class': 'form-control', 'id': 'id_education_level'}),
            'field_of_study': forms.Select(attrs={'class': 'form-control', 'id': 'id_field_of_study'}),
            'certification': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'expected_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'anything_else': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically adjust field_of_study choices based on education_level
        if self.instance and self.instance.education_level == 'Graduation':
            self.fields['field_of_study'].choices = JobApplication.GRADUATION_FIELDS
        elif self.instance and self.instance.education_level == 'Master':
            self.fields['field_of_study'].choices = JobApplication.MASTER_FIELDS



from django import forms
from .models import ContactUs, CompanyRegister

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'contact_number', 'message']

class CompanyRegisterForm(forms.ModelForm):
    class Meta:
        model = CompanyRegister
        fields = ['company_name', 'website', 'address', 'recruiter_name', 'recruiter_email', 'description']
