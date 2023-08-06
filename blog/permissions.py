from rest_framework.permissions import DjangoModelPermissions, BasePermission
from rest_framework.permissions import IsAuthenticated

from blog.models import Like, Post

class IsMyPostObject(BasePermission):
    """
    Permission class to check permission for own post instance
    """

    def has_permission(self, request, view):
        """
        function to check current user is owner of post object or not.
        """
        post_id = request.__dict__['parser_context']['kwargs']['id']
        instance = Post.objects.filter(id=post_id).first()
        if instance is not None:
            return instance.author.id == request._user.id


class IsMyLikeObject(BasePermission):
    """
    Permission class to check permission for own like instance
    """

    def has_permission(self, request, view):
        """
        function to check current user is owner of like object or not.
        """
        post_id = request.__dict__['parser_context']['kwargs']['id']
        instance = Like.objects.filter(id=post_id).first()
        if instance is not None:
            return instance.user.id == request._user.id

class IsAuthorizedForCreateLike(DjangoModelPermissions):
    """
    Custom permission for create like information
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return IsAuthenticated
        return True