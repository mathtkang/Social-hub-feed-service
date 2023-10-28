from django.urls import path
from posts import views

app_name = "posts"
# base_url: v1/posts/

urlpatterns =[
    path('<int:pk>/', views.PostsDetail.as_view()),
]
