from rest_framework import serializers
from users_manipulation.models import MyUser, MyUserHeadAddress, HeadMemberRealtion
from django.contrib.auth.models import Group
from users_manipulation.serializers import GroupSerializer

class ViewUserListSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    mobile_number = serializers.CharField(max_length=10)
    complete_address = serializers.CharField()

class VerifyMyuserInputSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10)

