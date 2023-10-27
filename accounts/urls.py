from django.urls import path
from .views import UserCreateView, UserActivationView, SendEmailView

app_name = "auth"
# base_url: v1/accounts/

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='user-create'),
    path('code/', UserActivationView.as_view(), name='user-activate'),
    path('<str:username>/', SendEmailView.as_view(), name='send-email'),
]