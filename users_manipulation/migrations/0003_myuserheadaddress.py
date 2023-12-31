# Generated by Django 4.2.3 on 2023-07-30 09:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_manipulation', '0002_alter_myuser_options_alter_myuser_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUserHeadAddress',
            fields=[
                ('MyUserHead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, to_field='mobile_number')),
                ('house_number', models.CharField(max_length=10)),
                ('floor_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('complete_address', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'HeadUserAddress',
            },
        ),
    ]
