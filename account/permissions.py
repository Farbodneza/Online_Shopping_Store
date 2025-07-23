from rest_framework.permissions import BasePermission


class IsProfileOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == obj or bool(request.user and request.user.is_staff):
            return True