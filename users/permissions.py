from rest_framework.permissions import BasePermission
from .models import User


class IsOwner(BasePermission):
    """Custom permission class to allow only bucketlist owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the user owner."""
        print('request user', request.user)
        print('request obj', obj)
        if isinstance(obj, User):
            return obj == request.user
        return obj == request.user
