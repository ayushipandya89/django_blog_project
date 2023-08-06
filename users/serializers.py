from rest_framework import serializers
from users.constants import PASSWORD_NOT_MATCH

from users.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer  for user registration
    """
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'password', 'password_confirmation']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        password_confirmation = validated_data.pop('password_confirmation')
        
        if password != password_confirmation:
            raise serializers.ValidationError({'password': [PASSWORD_NOT_MATCH]})
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer  for user details
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender']

class LoginSerializer(serializers.Serializer):
    """
    Serializer  for user login
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['username', 'password']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer  for user update
    """
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender']