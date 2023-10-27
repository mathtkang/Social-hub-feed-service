import random
import string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.core.mail import send_mail
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserCreateSerializer



# Create your views here.
'''
    username(해시태그)
    email 
    입력시 유저 생성 후 이메일 보냄
'''
#? /auth/registration/
class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    def perform_create(self, serializer):
        data = serializer.validated_data
        username = data['username']
        email = data['email']
        password = data['password']
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        user.auth_code = User.objects.create_auth_code()
        # message = f'가입 승인 코드: {user.auth_code}'
        user.save()
        # send_mail(subject, message, from_email)    #* 이메일 발송은 생략

        
        # Response 확인용
        response_data = {
            'username': username,
            'auth_code': user.auth_code,
            'from_email': email,
        }
        
        print("response_data: ", response_data)
        return Response(response_data, status = status.HTTP_201_CREATED)

#? /auth/code/
class UserActivationView(APIView): # 가입승인코드 확인
    serializer_class = UserSerializer
    def post(self, request):
        user =  request.data.get('username')
        auth_code = request.data.get('auth_code')  
        # email = request.data.get('email')
        user = User.objects.get(username=user)
        try:
            if  user.auth_code == auth_code:
                user.auth_code = None   # 인증된 유저는 인증코드 삭제
                user.is_active = True
                user.save()
                return Response({'message': '가입승인이 완료되었습니다.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': '올바르지 않은 가입승인 코드입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)