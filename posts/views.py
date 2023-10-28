from .models import Posts
from .serializers import PostSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

# Blog의 detail을 보여주는 역할
class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    
    # permission_classes = [IsAuthenticated, ]
    permission_classes = [AllowAny, ]
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = get_object_or_404(Posts, id=pk)
        #Posts에서 가지고온 query에서 해당 게시물 조회수를 가지고 옵니다.
        view_count = self.queryset.values().get(id=pk)['view_count']
        #get요청이 들어 올때 마다 해달 view_count를 +1합니다.
        view_count+=1
        instance.view_count = view_count
        instance.save()
        
        return self.retrieve(request, *args, **kwargs)