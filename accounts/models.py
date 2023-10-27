from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

class User(AbstractUser):
    objects = CustomUserManager()
    
    email = models.EmailField(verbose_name='email address')
    username = models.CharField(max_length=30, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_code = models.CharField(max_length=6, null=True, blank=True)
    

    ##user model에서 각 row를 식별해줄 key를 설정
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    #파이썬에서 어떤값(또는 객체)을 문자열로 변환하는데 사용하는 str()
    #내장 함수가 아닌 파이썬 내장 클래스
    def __str__(self):
        return self.email
    
    def get_hashtag(self):
        return f"#{self.username}"

    def is_authcode_certified(self):
        if self.auth_code:
            return False
        return True