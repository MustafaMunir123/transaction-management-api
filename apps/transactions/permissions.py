from rest_framework.permissions import BasePermission


class OnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        allowed_methods = ['GET']
        if request.user.id == 2:
            return True
        if request.method in allowed_methods:
            return True
        return False


class TransactionPermission(BasePermission):
    def has_permission(self, request, view):
        allowed_methods = ['GET', 'POST']
        if request.user.id == 2:
            return True
        if request.method in allowed_methods:
            return True
        return False
