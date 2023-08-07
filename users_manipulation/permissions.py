from rest_framework.permissions import BasePermission

# class AddmemberPermission(BasePermission):
#     def has_permission(self, request, view):
        
#         # return super().has_permission(request, view)
#         return request.user.groups.filter(name='verified_residents').exists() and request.user.groups.filter(name='family_head').exists()

class VerifiedResidentPermission(BasePermission):
    def has_permission(self, request, view):
        
        # return super().has_permission(request, view)
        return request.user.groups.filter(name='verified_residents').exists()
    
class FamilyHeadPermission(BasePermission):
    def has_permission(self, request, view):
        
        # return super().has_permission(request, view)
        return request.user.groups.filter(name='family_head').exists()

class FamilyMemberPermission(BasePermission):
    def has_permission(self, request, view):
        
        # return super().has_permission(request, view)
        return request.user.groups.filter(name='family_member').exists()
    
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, or OPTIONS requests (read-only) for any user.
        # if request.method in ['GET', 'HEAD', 'OPTIONS']:
        #     return True
        
        # Check if the user making the request is the owner of the object.
        return obj.mobile_number == request.user.mobile_number