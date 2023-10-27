import random
import string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import EmailMessage
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserCreateSerializer



# Create your views here.
#! /auth/registration/  -> 테스트용
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

        
        # Response 확인용
        response_data = {
            'username': username,
            'auth_code': user.auth_code,
            'from_email': email,
        }
        
        print("response_data: ", response_data)
        # send_mail(subject, message, from_email)    #* 이메일 발송은 생략 -> 회원생성과 동시에 이메일 발송할 경우
        return Response(response_data, status = status.HTTP_201_CREATED)

#? /auth/code/ : 가입승인코드 일치 확인
class UserActivationView(APIView): # 가입승인코드 확인
    serializer_class = UserSerializer
    def post(self, request):
        user =  request.data.get('username')
        auth_code = request.data.get('auth_code')  
        # email = request.data.get('email')   # 이메일 입력도 필요할 경우 사용
        try:
            user = User.objects.get(username=user)
            if  user.auth_code == auth_code:
                user.auth_code = None   # 인증된 유저는 인증코드 삭제
                user.is_active = True
                user.save()
                return Response({'message': '가입승인이 완료되었습니다.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': '올바르지 않은 가입승인 코드입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
#? /auth/<username>/ : username로 인증코드 메일전송 -> 이메일 재발송이 필요한경우
class SendEmailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer = UserSerializer
    lookup_field = 'username'

    def get(self, request, username):
        # user = self.get_queryset()
        user = get_object_or_404(User, username=username)
        if user.auth_code:
            try: 
                subject = "메일제목"
                email = user.email
                auth_code = user.auth_code
                to = [email]
                message = auth_code # 메일 내용  #최초 회원가입시도시 생성된 인증코드
                
                #* EmailMessage(subject=subject, body=message, to=to).send() # 메일 보내기
                
                # Response 확인용
                response_data = {
                    'subject': subject,
                    'message': message,
                    'to': to,
                }
                return Response({'메일 전송 완료':response_data}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': '메일 전송 중 오류가 발생했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': '사용자를 찾을 수 없거나 인증 코드가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_queryset(self):
        username = self.kwargs['username']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return 0
        
        return user