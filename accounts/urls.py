from django.urls import include, path
from . import views
from .views import CustomLoginView

app_name = "auth"
# base_url: v1/accounts/

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('', include('dj_rest_auth.urls'), name='dj_rest_auth'),
    path('registration/', include('dj_rest_auth.registration.urls'), name='registration'),
]