
from django.urls import include, path
from .views import UserApprovalView, SendEmailView, CustomLoginView


app_name = "auth"
# base_url: v1/auth/

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('', include('dj_rest_auth.urls'), name='dj_rest_auth'),
  #가입승인 url
    path('registration/', include('dj_rest_auth.registration.urls'), name='registration'),
    path('code/', UserApprovalView.as_view(), name='user-approval'),
    path('<str:username>/', SendEmailView.as_view(), name='send-email'),
]