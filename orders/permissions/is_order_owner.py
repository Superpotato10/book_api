from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOrderOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_manager

    def has_permission(self, request, view):
        return request.method in [*SAFE_METHODS, 'POST'] or request.user.is_manager
