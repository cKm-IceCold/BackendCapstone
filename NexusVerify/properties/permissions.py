from rest_framework.permissions import BasePermission

class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Company").exists()
            and obj.registered_by == request.user
        )


class IsAuditor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Auditor").exists()
        )
