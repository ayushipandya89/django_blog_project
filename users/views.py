from datetime import datetime
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from demo_project.permissions import IsAuthorizedForModel
from users.constants import INVALID_CREDENTIALS, NO_USER_FOUND
from users.models import User
from users.permissions import  IsAuthorizedForListUser, IsMyObject
from users.serializers import LoginSerializer, UserRegistrationSerializer, UserSerializer, UserUpdateSerializer
from django.contrib.auth.hashers import check_password
from users.utils import get_tokens_for_user
from demo_project import settings
from rest_framework.response import Response
from rest_framework import generics, status
from django.db.models import Q



# Create your views here.
class UserListCreateView(generics.ListCreateAPIView):
    """
    View for register user and list all user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthorizedForListUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['id', 'first_name', 'last_name', 'email', '-id', '-first_name', '-last_name', '-email']

    def get_serializer_class(self):
        """
        Returns serializer according to request.
        """
        if self.request.method == "GET":
            return UserSerializer
        else:
            return UserRegistrationSerializer


class LoginView(APIView):
    """
    class for user login 
    """

    def post(self, request, *args, **kwargs):
        """
        function to authenticate user
        """
        serializers = LoginSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist as e:
            raise ValidationError(NO_USER_FOUND) from e
        if not check_password(password, user.password):
            raise ValidationError(INVALID_CREDENTIALS)
        data = get_tokens_for_user(user)

        now = datetime.utcnow()

        # Calculate the expiry time based on the ACCESS_TOKEN_LIFETIME in the SIMPLE_JWT settings
        expiry_time = now + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        data.update(
            {'id': user.id,'email': user.email,'expires':expiry_time, 'first_name': user.first_name, 'last_name': user.last_name})
        return Response(data, status=status.HTTP_200_OK)


class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieve, update, delete employee.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorizedForModel, IsMyObject]
    lookup_field = 'id'
    

    def get_serializer_class(self):
        """
        Returns serializer according to request.
        """
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return UserUpdateSerializer
        else:
            return UserSerializer
