from rest_framework.permissions import BasePermission

class IsProfileOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_admin = request.user and request.user.is_staff
        return obj == request.user or is_admin