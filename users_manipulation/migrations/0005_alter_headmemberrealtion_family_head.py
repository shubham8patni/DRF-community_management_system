# Generated by Django 4.2.3 on 2023-08-01 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_manipulation', '0004_alter_myuser_aadhar_number_headmemberrealtion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headmemberrealtion',
            name='family_head',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_head', to=settings.AUTH_USER_MODEL, to_field='mobile_number'),
        ),
    ]