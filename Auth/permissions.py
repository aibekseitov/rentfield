from rest_framework.permissions import BasePermission
from Auth.models import User, Profile


class IsManager(BasePermission):
    def has_permission(self, request, view):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except:
            return False

        if (user_profile.type == Profile.Types.manager):
            return True