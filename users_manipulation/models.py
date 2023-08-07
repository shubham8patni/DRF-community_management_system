from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class MyUser(AbstractUser):
    username = models.CharField(("username"), max_length= 10, unique=False)
    mobile_number = models.CharField(unique=True, null=False, max_length=10, db_index=True)
    aadhar_number = models.CharField(unique=True, max_length=12, null = True)
    

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "mobile_number"
    

    class Meta:
        db_table = "CommunityMSUsers"

    # def __str__(self):
    #    return self.username


class MyUserHeadAddress(models.Model):
    MyUserHead = models.ForeignKey(MyUser, on_delete = models.CASCADE, to_field='mobile_number', primary_key=True)
    house_number = models.CharField(max_length=10)
    floor_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], null=False)
    complete_address = models.CharField(max_length=50, unique=True, null=False)

    class Meta:
        db_table = "HeadUserAddress"


class HeadMemberRealtion(models.Model):
    family_member = models.ForeignKey(MyUser, to_field="mobile_number", on_delete=models.CASCADE, related_name="family_member")
    family_head = models.ForeignKey(MyUser, on_delete=models.CASCADE, to_field="mobile_number", related_name="family_head")

    class Meta:
        db_table = "FamilyRelation"


