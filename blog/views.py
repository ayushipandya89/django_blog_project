from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from blog.constants import ALREADY_LIKED_POST, LIKE_DELETED_SUCCESSFULLY, LIKE_SAVED_SUCCESSFULLY, LIKE_UPDATED_SUCCESSFULLY, POST_CREATED_SUCCESSFULLY, POST_DELETED_SUCCESSFULLY, POST_UPDATED_SUCCESSFULLY
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from blog.models import Like, Post
from blog.permissions import IsAuthorizedForCreateLike, IsMyLikeObject, IsMyPostObject
from blog.serializers import LikeCreateSerializer, LikeSerializer, LikeUpdateSerializer, PostCreateSerializer, PostListSerializer, PostSerializer, PostUpdateSerializer
from demo_project.permissions import IsAuthorizedForModel
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

# Create your views here.
class PostCreateAPI(generics.CreateAPIView):
    """
    API view to create post
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        view to create post
        """
        request.data['author'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data, 'message': POST_CREATED_SUCCESSFULLY},
                        status=status.HTTP_201_CREATED)

class PostUpdateDeleteRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to update, delete and retrieve post
    """
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorizedForModel, IsMyPostObject]
    lookup_field = 'id'

    def get_serializer_class(self):
        """
        Returns serializer according to request.
        """
        if self.request.method == "PUT":
            return PostUpdateSerializer
        return PostSerializer
    
    def put(self, request, *args, **kwargs):
        """
        view to update post
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data, 'message': POST_UPDATED_SUCCESSFULLY},
                        status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        """
        view to delete post 
        """
        instance = self.get_object()
        instance.delete()
        return Response({'message': POST_DELETED_SUCCESSFULLY}, status=status.HTTP_204_NO_CONTENT)


class LikeCreateAPI(generics.ListCreateAPIView):
    """
    API to create like
    """
    queryset = Like.objects.all()
    permission_classes = [IsAuthorizedForCreateLike]

    def get_serializer_class(self):
        """
        Returns serializer according to request.
        """
        if self.request.method == "POST":
            return LikeCreateSerializer
        return LikeSerializer

    def post(self, request, *args, **kwargs):
        """"
        view to create like
        """
        instance = Like.objects.filter(post=request.data['post'], user= self.request.user)
        if instance:
            raise ValidationError({'like':ALREADY_LIKED_POST})
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data, 'message': LIKE_SAVED_SUCCESSFULLY},
                        status=status.HTTP_201_CREATED)


class LikeUpdateDeleteRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to update, delete and retrieve like
    """
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorizedForModel, IsMyLikeObject]
    lookup_field = 'id'

    def get_serializer_class(self):
        """
        Returns serializer according to request.
        """
        if self.request.method == "PUT":
            return LikeUpdateSerializer
        return LikeSerializer
    
    def put(self, request, *args, **kwargs):
        """
        view to update post
        """
        old_instance = Like.objects.filter(post=request.data['post'], user= self.request.user)
        if old_instance:
            raise ValidationError({'like':ALREADY_LIKED_POST})
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data, 'message': LIKE_UPDATED_SUCCESSFULLY},
                        status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        """
        view to delete post 
        """
        instance = self.get_object()
        instance.delete()
        return Response({'message': LIKE_DELETED_SUCCESSFULLY}, status=status.HTTP_204_NO_CONTENT)


class PostListAPI(generics.ListAPIView):
    """
    API to list post details
    """
    serializer_class = PostListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'author__first_name', 'author__last_name']
    ordering_fields = ['id','title' ,'author__first_name', 'author__last_name', '-id','-title', '-author__first_name', '-author__last_name']
    filterset_fields = ['type']


    def get_queryset(self):
        """
        override method to modify the queryset
        """
        queryset = Post.objects.annotate(num_likes=Count('liked_post')).select_related('author')
        if self.request.user.is_authenticated:
            if self.request.user.has_perm('blog.list_post'):
                queryset = queryset.filter(Q(author=self.request.user) | Q(type='public'))
        else:
            queryset = queryset.filter(type='public')
        return queryset

    def list(self, request, *args, **kwargs):
        """
        function to display list of post
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data':serializer.data})
