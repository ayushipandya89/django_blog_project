from rest_framework.permissions import DjangoModelPermissions, BasePermission
from rest_framework.permissions import IsAuthenticated
from users.constants import NO_USER_FOUND

from users.models import User


class IsAuthorizedForListUser(DjangoModelPermissions):
    """
    Custom permission for list users information
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return bool(request.user.has_perm('users.list_user') and IsAuthenticated)
        return True

class IsMyObject(BasePermission):
    """
    Permission class to check permission own user instance
    """

    def has_permission(self, request, view):
        """
        function to check current user is owner of object or not.
        """
        user_id = request.__dict__['parser_context']['kwargs']['id']
        instance = User.objects.filter(id=user_id).first()
        if instance is not None:
            return instance.id == request._user.id
