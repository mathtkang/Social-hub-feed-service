from django.urls import path
from posts import views

app_name = "posts"
# base_url: v1/posts/

urlpatterns =[
    path("", views.SearchPostsList.as_view()),
    path('<int:pk>/', views.PostsDetail.as_view()),
]

