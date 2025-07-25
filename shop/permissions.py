from rest_framework .permissions import BasePermission


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller
    

class IsShopOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user.store
        

class CanAddShopItem(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.store == request.user.store