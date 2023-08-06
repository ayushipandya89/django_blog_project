from rest_framework import serializers

from blog.models import Like, Post
from users.models import User

class UserDataSerializer(serializers.ModelSerializer):
    """
    serailizer to display details of user
    """
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']

    def to_representation(self, instance):
        """
        function to convert the response
        """
        rep = super(UserDataSerializer, self).to_representation(instance)
        rep['name'] = rep.pop('first_name') + " " + rep.pop('last_name')
        return rep
    

class PostCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create post
    """

    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'type']


class PostSerializer(serializers.ModelSerializer):
    """
    seralizer for post details
    """
    author = UserDataSerializer()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'type', 'date_posted', 'author']


class PostUpdateSerializer(serializers.ModelSerializer):
    """
    seralizer for update post details
    """
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'type']


class LikeCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create like details
    """

    class Meta:
        model = Like
        fields = ['post', 'user']


class LikeUpdateSerializer(serializers.ModelSerializer):
    """
    serializer to update like
    """

    class Meta:
        model = Like
        fields = ['post']


class LikeSerializer(serializers.ModelSerializer):
    """
    serializer to display like details of post
    """
    post = PostSerializer()

    class Meta:
        model = Like
        fields = ['id', 'timestamp', 'post']


class PostListSerializer(serializers.ModelSerializer):
    """
    serializer to listing details of post
    """
    author = UserDataSerializer()
    num_likes = serializers.IntegerField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'author', 'type', 'num_likes']