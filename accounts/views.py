from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomLoginSerializer  # 커스텀 시리얼라이저를 가져옴

class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer  # 커스텀 시리얼라이저를 사용

    def post(self, request, *args, **kwargs):
        # 로그인 로직을 그대로 유지
        return super(CustomLoginView, self).post(request, *args, **kwargs)