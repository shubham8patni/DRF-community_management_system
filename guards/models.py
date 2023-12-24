from django.db import models

# Create your models here.


class GateTrafficLog(models.Model):
    guard_name = models.CharField(null=False, max_length=50)
    guard_mobile_number = models.CharField(null=False, max_length=10)
    guard_aadhar =  models.CharField(unique=True, max_length=12, null = True) # later replace by aadhar document link
    traffic_description = models.CharField(max_length=50, null=False)
    person_allowed_name = models.CharField(null=False, max_length=50)
    person_allowed_number = models.CharField(null=False, max_length=10)
    person_allowed_adhar = models.CharField(unique=True, max_length=12, null = True) # later replace by aadhar document link
    family_head_name = models.CharField(null=False, max_length=50)
    family_head_number = models.CharField(null=False, max_length=10)
    family_head_adhar = models.CharField(unique=True, max_length=12, null = True) # later replace by aadhar document link
    complete_address = models.CharField(max_length=50, null=False)
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        # app_label = 'app_label'
        db_table = 'GateTrafficLog'
        managed = False
        # using = 'mysql-docker-django-2'  # Specify the 'default' database for reading
        # db_name = "logg_traffic"
        