from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'auth_code']
        extra_kwargs = {
            'email': {'read_only': True},  
        }

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'auth_code']
        extra_kwargs = {
            'auth_code': {'read_only': True},  
        }
