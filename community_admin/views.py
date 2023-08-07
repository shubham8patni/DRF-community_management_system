from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from users_manipulation.models import MyUser, MyUserHeadAddress
from users_manipulation.serializers import GetMyUserProfileSerializer
from .serializers import ViewUserListSerializer, VerifyMyuserInputSerializer
from .permissions import AdminOnlyPermission
from django.db.models import Q, F

# Create your views here.
# class GetMyUserList(views.APIView):
#     # permission_classes=[AdminOnlyPermission]
#     def get(self, request, category):
#         allowed_groups = Group.objects.exclude(name = "management").values("name")
#         allowed_groups_list = [x['name'] for x in allowed_groups]

#         if category in allowed_groups_list: #['unverified_guard', 'unverified_resident', 'verified_guard', 'verified_resident']:
#             pass
#         else:
#             return Response({
#                 "status" : 400,
#                 "body" : "invalid category"
#             })
#         #### GET INFO FROM DB ####
#         address_list = MyUser.objects.filter(groups__name=category).annotate(complete_address=F('myuserheadaddress__complete_address')).values('mobile_number', 'first_name', 'complete_address')
#         #### ADVANCE ORM AND SQL QUERY for above 2 queries
#         # MyUser.objects.filter(groups__name='unverified_resident').annotate(complete_address=F('myuserheadaddress__complete_address')).values('mobile_number', 'first_name', 'complete_address')
#         # select MyUser.mobile_number, MyUser.first_name, MyUserHeadAddress.completeAddress from MyUser left join MyUserHeadAddress on Myuser.mobile_number = MyUserHeadAddress.MyUserHead where MyUser.groups = category
        
#         address_list = [{'mobile_number': item['mobile_number'], 'first_name': item['first_name'], 'complete_address': item['complete_address']} for item in address_list if item['first_name'] != "" and item['complete_address'] is not None]
#         serializer_class = ViewUserListSerializer(data = address_list, many = True, partial = True)
#         if serializer_class.is_valid():
#             return Response({
#                 "status" : 200,
#                 "body" : serializer_class.data
#             })
#         else:
#             return Response({
#                     "status" : 401,
#                     "body" : serializer_class.errors
#                 })


class GetMyUserList(generics.ListAPIView):
    serializer_class = ViewUserListSerializer
    lookup_field = "groups"

    def get_queryset(self):
        group = self.kwargs['groups']
        if group == "unverified_guard" or group == "verified_guard" :
            queryset = MyUser.objects.filter(groups__name = group)
        elif group == "unverified_resident":
            queryset = MyUser.objects.filter(groups__name=group, myuserheadaddress__complete_address__isnull=False).annotate(complete_address=F('myuserheadaddress__complete_address')).values('mobile_number', 'first_name', 'complete_address')
        else:
            queryset = "Error"
        return queryset
    

class VerifyMyUser(views.APIView):
    http_method_names = ['post']
    serializer_class = VerifyMyuserInputSerializer
    def post(self, request):
        serialized_input = VerifyMyuserInputSerializer(data = request.data)
        if serialized_input.is_valid():
            mobile_number = serialized_input.data['mobile_number']
        else:
            return Response({
                "error" : serialized_input.errors
            })

        user_info = MyUser.objects.get(mobile_number = mobile_number)
        user_group = user_info.groups.all()
        user_group_list = [group.name for group in user_group]
        if 'unverified_resident' in  user_group_list:
            new_group = Group.objects.get(name = "verified_resident")
            new_group2 = Group.objects.get(name = "family_head")
            # Clear all groups assigned to the user
            user_info.groups.clear()
            # user_info.groups.remove(user_group[0].id)
            user_info.groups.add(new_group, new_group2)
        elif 'unverified_guard' in  user_group_list:
            new_group = Group.objects.get(name = "verified_guard")
            # Clear all groups assigned to the user
            user_info.groups.clear()
            # user_info.groups.remove(user_group)
            user_info.groups.add(new_group, new_group2)
        else:
            return Response({
                "status" : 401,
                "message" : "can not verify user!",
                "debug" : user_group_list
            })
        
        return Response({
                "status" : 201,
                "message" : "user verified!",
                "data" : [group for group in (MyUser.objects.filter(mobile_number = mobile_number).annotate(user_groups = F('groups__name')).values('mobile_number', 'first_name', 'user_groups'))]
            })
    

class MyUserVerify(generics.RetrieveUpdateAPIView):
    serializer_class = GetMyUserProfileSerializer
    queryset = MyUser.objects.all()
    lookup_field = "mobile_number"
    http_method_names = ['get', 'patch']

    def patch(self, request, mobile_number):
        if request.user.groups.filter(name = "unverified_resident").exists():
            # return Response(str(request.user.groups.filter(name = "unverified_resident").exists))
            group1 = Group.objects.get(name = "verified_resident")
            group2 = Group.objects.get(name = "family_head")
        elif request.user.groups.filter(name = "unverified_guard").exists():
            group1 = Group.objects.get(name = "verified_guard")
            group2 = None
        else:
            return Response({
                "status" : 401,
                "error" : "invalid group"
            })
        user_instance = MyUser.objects.get(mobile_number = mobile_number)
        user_instance.groups.clear()
        user_instance.groups.add(group1, group2)
        user_instance_serialized = GetMyUserProfileSerializer(user_instance)
        return Response({
                "status" : 201,
                "message" : "user verified successfully",
                "data" : user_instance_serialized.data
            })
    


# class UpdateUserGroup(views.APIView):
#     http_method_names = ['patch']

#     def patch(self.request):
        

#         if 'unverified_resident' in  user_group_list:
#             new_group = Group.objects.get(name = "verified_resident")
#             new_group2 = Group.objects.get(name = "family_head")
#             # Clear all groups assigned to the user
#             user_info.groups.clear()
#             # user_info.groups.remove(user_group[0].id)
#             user_info.groups.add(new_group, new_group2)
#         elif 'unverified_guard' in  user_group_list:
#             new_group = Group.objects.get(name = "verified_guard")
#             # Clear all groups assigned to the user
#             user_info.groups.clear()
#             # user_info.groups.remove(user_group)
#             user_info.groups.add(new_group, new_group2)
#         pass