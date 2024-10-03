from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owner of an object to edit it
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj == request.user:
            return True
        
        # Handle edit/delete operations
        elif obj == request.user:
            return True