# Generated by Django 4.2.3 on 2023-07-29 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_manipulation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={},
        ),
        migrations.AlterModelTable(
            name='myuser',
            table='CommunityMSUsers',
        ),
    ]
