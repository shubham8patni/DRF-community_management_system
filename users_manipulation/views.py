from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterMyUserSerializer, CreateHeadAddressSerializer, UpdateUserProfileSerializer, AddFamilymembersSerializer, GetMyUserProfileSerializer, AddFamilymembersUpdateProfileSerializer, GroupSerializer, LoginMyUserSerializer
from .models import MyUser, MyUserHeadAddress, HeadMemberRealtion
from django.contrib.auth.models import Group
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly, VerifiedResidentPermission, FamilyHeadPermission  #AddmemberPermission, 
from .helper_function import password_generate, aadharNumVerify
from django.urls import reverse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import logout
# from rest_framework.authtoken.models import Token # DRF in built basic authenctication

# import requests

# Create your views here.

class GetgroupList(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

class RegisterMyuser(generics.CreateAPIView):
    serializer_class = RegisterMyUserSerializer
     
    def post(self, request):
        serialized_data = RegisterMyUserSerializer(data = request.data)
        print("*******************************************************************************************")
        # print(serialized_data)
        if serialized_data.is_valid():
            user_instance = serialized_data.save()
            # auth_token = Token.objects.create(user=user_instance) # DRF in built basic authenctication
            auth_token = RefreshToken.for_user(user_instance)
            return Response({
                'status' : 201,
                "refresh_token" : str(auth_token),
                "access_token" : str(auth_token.access_token),
                "response" : "user created successfully!",
            })
        else:
            return Response({
                'error' : serialized_data.errors

            })
        
# token = Token.objects.create(user=...)

class UpdateUserProfile(generics.UpdateAPIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UpdateUserProfileSerializer
    http_method_names = ['patch']
    # queryset = MyUser.objects.all()
    lookup_field = 'mobile_number'
    
    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            print(e)
            return e

    def partial_update(self, request, mobile_number):
        not_allowed_groups = []
        if request.data['groups'][0] not in not_allowed_groups:
            user_instance = MyUser.objects.get(mobile_number = mobile_number)
            group_name = request.data.pop('groups')
            
            if user_instance.groups.all().exists():
                # request.data['groups'] = [group.id for group in user_instance.groups.all()]
                pass
            else:
                group_instance = Group.objects.get(name = group_name[0])
                user_instance.groups.add(group_instance)
                # request.data['groups'] = [group_instance.id]
            
            serialized_data = UpdateUserProfileSerializer(user_instance, data = request.data, partial=True)
            
            if serialized_data.is_valid():
                
                try:
                    
                    self.perform_update(serialized_data)
                    
                    return Response({
                        "status" : status.HTTP_200_OK,
                        "response" : serialized_data.data, 
                    })
                except:
                    return Response({
                        "error" :  "something went wrong"
                    })
            else:
                return Response({
                            "error" :  serialized_data.errors #"insufficient priveleges"
                        })
        else:
            return Response({
                            "error" :  "insufficient priveleges"
                        })
        
class CreateHeadAddress(generics.CreateAPIView):
    serializer_class = CreateHeadAddressSerializer
    # permission_classes = [VerifiedResidentPermission, FamilyHeadPermission]
    queryset = MyUserHeadAddress.objects.all()
    http_method_names = ['post']
    # permission_classes = [AddmemberPermission]



class AddFamilyMembers(views.APIView):
    serializer_class = AddFamilymembersSerializer
    # permission_classes = [VerifiedResidentPermission, FamilyHeadPermission]  #[AddmemberPermission]
    http_method_names = ['post']

    def post(self, request):

        serialized_data = AddFamilymembersSerializer(data = request.data, partial = True)
        
        if serialized_data.is_valid():
            head_user_instance = MyUser.objects.get(mobile_number=serialized_data.data['family_head_mobile_number'])
            #### REGISTER MEMBER USER AND GENERATE PASSWORD ####
            register_user_info = {}
            register_user_info['mobile_number'] = serialized_data.data['member_mobile_number']
            register_user_info['password'] = password_generate(serialized_data.data['member_mobile_number'], serialized_data.data['first_name'])
            registered_serializer_instance = RegisterMyUserSerializer(data = register_user_info)
            if registered_serializer_instance.is_valid():
                registered_member_instance = registered_serializer_instance.save()
            else:
                return Response( {
                    "error" : registered_serializer_instance.errors
                } )
            #### REGISTER MEMBER USER AND GENERATE PASSWORD ####

            #### ADD MEMBER USER GROUP ####
            member_user_group = Group.objects.get(name = "verified_resident")
            member_group = Group.objects.get(name = "family_member")
            registered_member_instance.groups.add(member_user_group, member_group)
            # registered_member_instance.groups.add(member_group)
            #### ADD MEMBER USER GROUP ####

            #### UPDATE NEW MEMBER PROFILE INFO ####
            profile = {}
            profile['first_name'] = serialized_data.data['first_name']
            profile['last_name'] = serialized_data.data['last_name']
            profile['aadhar_number'] = serialized_data.data['aadhar_number']
            serialized_profile_update = AddFamilymembersUpdateProfileSerializer(registered_member_instance, data = profile, partial = True)
            if serialized_profile_update.is_valid():
                serialized_profile_update.save()
            else:
                return Response({
                    "error" : serialized_profile_update.errors
                })
            #### UPDATE NEW MEMBER PROFILE INFO ####

            member_user_instance = MyUser.objects.get(mobile_number=serialized_data.data['member_mobile_number'])
            
            # Create a new HeadMemberRealtion instance and set the family_head and family_member fields
            relation_instance = HeadMemberRealtion.objects.create(
                family_head=head_user_instance,
                family_member=member_user_instance
            )
            # Save the relation instance
            try:
                relation_instance.save()
                return Response({
                    "message": "Family relation created successfully"}, status=status.HTTP_201_CREATED)
            except:
                return Response({
                    "message" : relation_instance
                }, 
                status=status.HTTP_400_BAD_REQUEST
                )
        return Response({
                "message" : serialized_data.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
            )

       

class GetMyUserProfile(generics.RetrieveAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    model = MyUser
    lookup_field = "mobile_number"
    serializer_class = GetMyUserProfileSerializer
    queryset = MyUser.objects.all()


class LoginUser(views.APIView):
    # serializer_class = LoginMyUserSerializer
    def post(self, request):
        try:
            serialized_data = LoginMyUserSerializer(data = request.data)
            if serialized_data.is_valid():
                user = authenticate(username = serialized_data.validated_data['phone_number'], password = serialized_data.validated_data['password'])
                auth_token = RefreshToken.for_user(user)
                return Response({
                    "status" : 201,
                    "refresh_token" : str(auth_token),
                    "access_token" : str(auth_token.access_token)
                })
        except Exception as e:
            return Response({
                "error": str(e)
            })
        return Response({
                "message" : serialized_data.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
            )


def logout_view(request):
    logout(request)
    return Response({
        "message" : "logged out!"
    })
# {
# "mobile_number" : "9999999999",
# "house_number" : "B-11", 
# "floor_number" : 0, 
# "complete_address" : "B-11 0"
# }

# {
# "MyUserHead" : "9999999998",
# "house_number" : "B-11", 
# "floor_number" : 0, 
# "complete_address" : "B-11 Ground Floor"
# }

# {
#     "groups": [
#         "unverified_resident"
#     ],
#     "first_name": "test99",
#     "last_name": "user",
#     "aadhar_number": "123412341234"
# }
