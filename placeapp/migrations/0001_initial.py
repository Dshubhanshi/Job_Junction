# Generated by Django 5.1.2 on 2024-11-13 15:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(max_length=20)),
                ('website', models.URLField()),
                ('company_picture', models.ImageField(blank=True, null=True, upload_to='company_pictures/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=15)),
                ('dob', models.DateField()),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('profile_picture', models.ImageField(default='profile_pictures/default.png', upload_to='profile_pictures/')),
                ('role', models.CharField(choices=[('student', 'Student'), ('recruiter', 'Recruiter')], max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyRecruiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placeapp.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlacementSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placement_sessions', to='placeapp.company')),
                ('recruiter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_sessions', to='placeapp.companyrecruiter')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=100)),
                ('year_of_graduation', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_selected', models.CharField(default='2024-11-13', max_length=10)),
                ('status', models.CharField(choices=[('Selected', 'Selected'), ('Pending', 'Pending')], max_length=50)),
                ('placement_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selections', to='placeapp.placementsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selections', to='placeapp.student')),
            ],
        ),
        migrations.AddField(
            model_name='placementsession',
            name='students_attending',
            field=models.ManyToManyField(blank=True, related_name='attended_sessions', to='placeapp.student'),
        ),
        migrations.CreateModel(
            name='JobOpening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_openings', to='placeapp.company')),
                ('recruiter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_jobs', to='placeapp.companyrecruiter')),
                ('students_applied', models.ManyToManyField(blank=True, related_name='applied_jobs', to='placeapp.student')),
            ],
        ),
    ]
