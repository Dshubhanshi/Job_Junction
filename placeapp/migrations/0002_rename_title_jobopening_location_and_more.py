import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('placeapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobopening',
            old_name='title',
            new_name='location',
        ),
        migrations.RemoveField(
            model_name='jobopening',
            name='recruiter',
        ),
        migrations.RemoveField(
            model_name='jobopening',
            name='students_applied',
        ),
        migrations.RemoveField(
            model_name='placementsession',
            name='recruiter',
        ),
        migrations.RemoveField(
            model_name='placementsession',
            name='students_attending',
        ),
        migrations.RemoveField(
            model_name='selection',
            name='date_selected',
        ),
        migrations.AddField(
            model_name='jobopening',
            name='position',
            field=models.CharField(default='Software Engineer', max_length=100),  # Provide a sensible default
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobopening',
            name='posted_on',
            field=models.DateField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobopening',
            name='qualification',
            field=models.CharField(default='Bachelor\'s Degree', max_length=255),  # Provide a sensible default
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='placementsession',
            name='students_selected',
            field=models.ManyToManyField(through='placeapp.Selection', to='placeapp.Student'),
        ),
        migrations.AddField(
            model_name='selection',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='placementsession',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placeapp.Company'),
        ),
        migrations.AlterField(
            model_name='selection',
            name='placement_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placeapp.PlacementSession'),
        ),
        migrations.AlterField(
            model_name='selection',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selection',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placeapp.Student'),
        ),
    ]
