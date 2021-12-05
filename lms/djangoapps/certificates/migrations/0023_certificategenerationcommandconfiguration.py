# Generated by Django 2.2.19 on 2021-03-30 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certificates', '0022_add_unique_constraints_to_certificatewhitelist_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateGenerationCommandConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('arguments', models.TextField(blank=True, default='', help_text="Arguments for the 'cert_generation' management command. Specify like '-u <user_id> -c <course_run_key>'")),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
            options={
                'verbose_name': 'cert_generation argument',
            },
        ),
    ]
