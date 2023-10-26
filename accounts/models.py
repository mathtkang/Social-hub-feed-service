import string
import random

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


STRING_SEQUENCE = string.ascii_uppercase + string.digits


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("username은 필수 영역입니다.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.auth_code = UserManager.create_auth_code()
        user.save(using=self._db)
        return user
            
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)
    
    @classmethod
    def create_auth_code(cls):
        auth_code = ""
        for _ in range(6):
            auth_code += random.choice(STRING_SEQUENCE)
        
        return auth_code


class User(AbstractUser):
    objects = UserManager()
    auth_code = models.CharField(null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def get_hashtag(self):
        return f"#{self.username}"

    def is_authcode_certified(self):
        if self.auth_code:
            return False
        return True
