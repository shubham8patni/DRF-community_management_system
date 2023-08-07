from rest_framework.permissions import BasePermission

class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        # return super().has_permission(request, view)
        return request.user.groups.filter(name='management').exists()