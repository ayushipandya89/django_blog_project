from django.urls import path

from users.views import LoginView, UserListCreateView, UserRetrieveUpdateDeleteView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('login', LoginView.as_view(), name='login'),
    path('employee/<int:id>/', UserRetrieveUpdateDeleteView.as_view(),
         name="retrieve_update_delete_user"),

]