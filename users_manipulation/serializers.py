from rest_framework import serializers
from .models import MyUser, MyUserHeadAddress, HeadMemberRealtion
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]

class HeadAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUserHeadAddress
        fields = ["house_number", "floor_number", "complete_address"]

class RegisterMyUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = ['mobile_number', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    # groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    class Meta:
        model = MyUser
        fields = ["groups", "first_name", "last_name", "aadhar_number"] #   "mobile_number",

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if "groups" in data:
            data.pop('groups')  # Remove the 'groups' field from the serialized data
        else:
            pass
        return data

class CreateHeadAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUserHeadAddress
        fields = ['MyUserHead','house_number', 'floor_number', 'complete_address']

    def create(self, validated_data):
        mobile_number = validated_data.pop('MyUserHead')
        try:
            user = MyUser.objects.get(mobile_number=mobile_number)
        except MyUser.DoesNotExist:
            raise Exception(MyUser.DoesNotExist)
        validated_data['MyUserHead'] = user
        return super().create(validated_data)
        
class AddFamilymembersSerializer(serializers.Serializer):
    family_head_mobile_number = serializers.CharField(required = True, max_length=10)
    member_mobile_number = serializers.CharField(required = True, max_length=10)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    aadhar_number = serializers.CharField(max_length=12, required = True)

class AddFamilymembersUpdateProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = ["first_name", "last_name", "aadhar_number"]

    def update(self, instance, validated_data):
        # Remove the fields you don't want to update from the validated data
        # Here, 'field1' and 'field2' are the fields you don't want to update
        # validated_data.pop('field1', None)
        # validated_data.pop('field2', None)

        # Perform the update using the remaining data
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # Save the updated instance to the database
        # instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class GetMyUserProfileSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    groups = GroupSerializer(many = True) #serializers.SerializerMethodField() #
    class Meta:
        model = MyUser
        fields = ["mobile_number", "first_name", "last_name", "aadhar_number", "groups", "email", "username", "date_joined", "address"]

    def get_address(self, instance):
        try:
            head_address_instance = MyUserHeadAddress.objects.get(MyUserHead=instance)
            serializer = HeadAddressSerializer(head_address_instance)
            return serializer.data
        except MyUserHeadAddress.DoesNotExist:
            return None
    
    # def get_groups(self, instance):
    #     groups =instance.groups.get()
    #     group_s = GroupSerializer(groups)
    #     # if group_s.is_valid():
    #     return group_s.data
    #     # else:
    #     #     return group_s.errors

class LoginMyUserSerializer(serializers.Serializer):    
    phone_number = serializers.CharField(required = True)
    password = serializers.CharField(required = True)