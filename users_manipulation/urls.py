from django.contrib import admin
from django.urls import path, include
from .views import RegisterMyuser, UpdateUserProfile, CreateHeadAddress, AddFamilyMembers, GetMyUserProfile, GetgroupList, LoginUser, logout_view
from rest_framework.authtoken import views
urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('register/', RegisterMyuser.as_view(), name = "register"),
    path('update/<str:mobile_number>', UpdateUserProfile.as_view(), name = "update-profile"),
    path('create_head_address/', CreateHeadAddress.as_view(), name = "create-head-address"),
    path('add_family/', AddFamilyMembers.as_view(), name = "add-damily-members"),
    path('get_profile/<str:mobile_number>', GetMyUserProfile.as_view(), name = "get-single-profile"),
    path('groups_list/', GetgroupList.as_view(), name = "group-list"),
    path('login/', LoginUser.as_view(), name = "login"),
    path('logout/', logout_view, name = "logout"),
]


