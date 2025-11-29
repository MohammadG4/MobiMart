from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins can access anything
        if request.user.is_staff:
            return True
        
        # Users can only access their own data
        return obj.id == request.user.id