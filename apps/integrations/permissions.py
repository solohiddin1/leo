from django.conf import settings
from rest_framework.permissions import BasePermission


class InternalServicePermission(BasePermission):
    """Gate for server-to-server endpoints used by usta-source (no JWT-authenticated
    leo user exists for a Telegram bot request) — a shared secret takes the place of
    ClientPermission's `request.user.is_verified` check."""

    def has_permission(self, request, view):
        token = request.headers.get("X-Internal-Token", "")
        expected = getattr(settings, "INTERNAL_API_TOKEN", "")
        return bool(expected) and token == expected
