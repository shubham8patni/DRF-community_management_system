from django.urls import path
from .views import GetMyUserList, MyUserVerify #VerifyMyUser

urlpatterns = [
    path('userslist/<str:groups>', GetMyUserList.as_view(), name="user-listy"),
    path('verify/<str:mobile_number>', MyUserVerify.as_view(), name="user"),
]
