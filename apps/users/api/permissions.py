# Third Party Imports
from rest_framework.permissions import BasePermission


class IsAuthenticatedAndAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user:
                if request.user.is_admin:
                    return True
                raise PermissionError("Not an admin user")
            return False
        except Exception as ex:
            raise ex
