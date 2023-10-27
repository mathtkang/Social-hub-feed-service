from django.urls import path
from .views import UserCreateView, UserActivationView

app_name = "accounts"
# base_url: v1/accounts/

urlpatterns = [
    path('auth/registration/', UserCreateView.as_view(), name='user-create'),
    path('auth/code/', UserActivationView.as_view(), name='user-activate'),
]