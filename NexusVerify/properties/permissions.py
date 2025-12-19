from rest_framework.permissions import BasePermission

class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Company").exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.registered_by == request.user
