
from rest_framework import serializers
from .models import CustomUserManager
from django.contrib.auth import get_user_model

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
##연습용 Serializer
from rest_framework.serializers import ModelSerializer
from datetime import datetime


class UserApprovalSerializer(ModelSerializer):
    class Meta:
model = get_user_model()
        fields = ['username', 'email', 'auth_code']
        read_only_fields = ['email']

class CustomRegisterSerializer(RegisterSerializer):
    def save(self, request):
        user = super().save(request)  # userame, email, password는 RegisterSerializer에서 진행됨
        # 사용자 생성 이후에 인증 코드를 설정
        user.auth_code = CustomUserManager.create_auth_code()
        user.save()

        return user

class CustomLoginSerializer(LoginSerializer):
    # email 필드를 제거
    email = None
