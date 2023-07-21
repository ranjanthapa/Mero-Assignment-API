from rest_framework.permissions import BasePermission
from .models import Group


class IsGroupAdmin(BasePermission):
    def has_object_permission(self, request, view, obj: Group):
        return obj.admin == request.user.userprofile


class IsGroupMember(BasePermission):
    def has_object_permission(self, request, view, obj: Group):
        if request.method == "GET" and request.user.get_username() in obj.members.all():
            return True
        return False
