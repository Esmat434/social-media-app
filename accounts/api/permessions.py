from rest_framework.permissions import BasePermission

class isAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
class isNotAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        return not (request.user and request.user.is_authenticated)
