from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import date
import string
import random

STRING_SEQUENCE = string.ascii_uppercase + string.digits # 새로운 인증 코드 생성

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    #일반 유저 생성
    def create_user(self,username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError("username은 필수 영역입니다.")
        #email 형태를 동일하게 만들기 위한 함수
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields)
        
        user.auth_code = self.create_auth_code()
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    @classmethod
    def create_auth_code(cls):
        auth_code = ""
        for _ in range(6):
            auth_code += random.choice(STRING_SEQUENCE)
        return auth_code

    
    #관리자 유저 생성
    def create_superuser(self,username,  email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(username, email, password, **extra_fields)