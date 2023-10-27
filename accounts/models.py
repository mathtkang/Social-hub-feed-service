import string
import random

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


STRING_SEQUENCE = string.ascii_uppercase + string.digits


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("username은 필수 영역입니다.")
        if not email:
            raise ValueError("email은 필수 영역입니다.")
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.auth_code = self.create_auth_code()
        user.save(using=self._db)
        return user
            
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username=username, email=email, password=password, **extra_fields)
    
    @classmethod
    def create_auth_code(cls):
        auth_code = ""
        for _ in range(6):
            auth_code += random.choice(STRING_SEQUENCE)
        return auth_code


class User(AbstractUser):
    objects = UserManager()
    auth_code = models.CharField(null=True, blank=True, max_length=10)
    
    USERNAME_FIELD = 'username'  # 해시태그
    REQUIRED_FIELDS = ['email']
    
    def get_hashtag(self):
        return f"#{self.username}"

    def is_authcode_certified(self):
        if self.auth_code:  #인증 코드가 있다면(미인증된 유저)
            return False
        return True