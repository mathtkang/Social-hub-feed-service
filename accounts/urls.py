
from django.urls import include, path
from .views import UserActivationView, SendEmailView, CustomLoginView
from . import views


app_name = "auth"
# base_url: v1/accounts/

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('', include('dj_rest_auth.urls'), name='dj_rest_auth'),
  #가입승인 url
    path('code/', UserActivationView.as_view(), name='user-activate'),
    path('<str:username>/', SendEmailView.as_view(), name='send-email'),
    path('registration/', include('dj_rest_auth.registration.urls'), name='registration'),
]