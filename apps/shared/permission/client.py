from rest_framework.permissions import BasePermission


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return bool(request.user.is_verified and request.user.is_active)
