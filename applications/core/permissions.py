from rest_framework import permissions

class IsEmployerPermisson(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'is_employer'
      