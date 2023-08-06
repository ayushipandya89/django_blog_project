from django.urls import path

from blog.views import LikeCreateAPI, LikeUpdateDeleteRetrieveAPI, PostCreateAPI, PostListAPI, PostUpdateDeleteRetrieveAPI


urlpatterns = [
    path('post', PostCreateAPI.as_view(), name='post-create'),
    path('post/<int:id>/', PostUpdateDeleteRetrieveAPI.as_view(), name='post-update-retrieve-delete'),
    path('post/list', PostListAPI.as_view(), name='post-list'),
    path('like', LikeCreateAPI.as_view(), name='like-create'),
    path('like/<int:id>/', LikeUpdateDeleteRetrieveAPI.as_view(), name='like-update-delete-retrieve'),


]