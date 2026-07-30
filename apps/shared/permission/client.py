from rest_framework.permissions import BasePermission

from apps.user.models import User


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user is None:
            return False

        db_user = User.objects.get(pk=request.user.id)
        if db_user.is_verified and db_user.is_active:
            return True
        return False
