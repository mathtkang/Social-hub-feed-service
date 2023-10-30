import requests
from rest_framework import generics, status, filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from itertools import product
from django.shortcuts import render

from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination

from posts.models import Posts, HashTags, SNSType
from posts.serializers import PostSerializer, ShareSerializer

# Blog의 detail을 보여주는 역할
class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    
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

## constants
ORDER_BY = [s+o for s, o in list(product(['-', ''],['created_at', 'updated_at','like_count','share_count', 'view_count']))]


class PostsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class SearchPostsList(ListAPIView):
    permission_classes = [AllowAny]
    
    serializer_class = PostSerializer
    pagination_class = PostsPagination
    
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = Posts.objects.all()

        # hashtag, type, order_by, search_by, search 파라미터 처리
        query_params = self.request.query_params
        hashtag = query_params.get('hashtag', self.request.user.username)

        if hashtag:
            queryset = queryset.filter(hashtags__name__exact=hashtag)

        post_type = query_params.get('type', None)
        if post_type:
            queryset = queryset.filter(type=post_type)

        order_by = query_params.get('order_by', 'created_at')
        if order_by not in ORDER_BY:
            raise ValueError(f'oreder_by 변수는 {ORDER_BY}중 하나이어야 합니다.')
        queryset = queryset.order_by(order_by)

        search_by = query_params.get('search_by', 'title,content')
        keyword = query_params.get('search')
        if search_by and keyword:
            search_by_list = search_by.split(',')
            search_filter = dict()
            for by in search_by_list:
                search_filter[f'{by}__icontains'] = keyword
            queryset = queryset.filter(**search_filter)

        return queryset


class LikeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        post = Posts.objects.get(id=pk)
        sns = post.type
        content_id = post.content_id
        
        if sns == 'facebook':
            api_url = f'https://www.facebook.com/likes/{content_id}'
        elif sns == 'twitter':
            api_url = f'https://www.twitter.com/likes/{content_id}'
        elif sns == 'instagram':
            api_url = f'https://www.instagram.com/likes/{content_id}'
        elif sns == 'threads':
            api_url = f'https://www.threads.com/likes/{content_id}'
        else:
            raise
        
        post.like_count += 1
        post.save()
        
        response = requests.get(api_url)

        IS_LOCAL = True
        if response.status_code == 200 or IS_LOCAL:
            return Response(
                {
                    'message': f'{sns} 게시글에 좋아요 개수가 올라갔습니다.',
                    'like_count': post.like_count,
                }, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message': 'API 요청 실패'
                }, 
                status=status.HTTP_400_BAD_REQUEST,
            )


# 공유 api 호출
class SharePosts(APIView):
    serializer_class = ShareSerializer
    def post(self, request, pk):
        try:
            post = Posts.objects.get(pk=pk)
            url = ''
            # type을 기반으로 URL을 생성한다.
            if post.type == SNSType.FACEBOOK.value:
                url = f'https://www.facebook.com/share/{post.content_id}'
            elif post.type == SNSType.TWITTER.value:
                url = f'https://www.twitter.com/share/{post.content_id}'
            elif post.type == SNSType.INSTAGRAM.value:
                url = f'https://www.instagram.com/share/{post.content_id}'
            elif post.type == SNSType.THREAD.value:
                url = f'https://www.threads.net/share/{post.content_id}'
            else:
                return Response({'message': 'SNS타입이 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            IS_TEST = True
            response = requests.post(url, data={'share_count': 1}) # 실제 동작은 안함
            if response.status_code == 200 or IS_TEST:
                post.share_count += 1 
                post.save()
                response_data = {
                                'message': '공유 성공',
                                'share_count': post.share_count,
                                'sns_type' : post.type,
                                'url': url,
                                }   
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'API 요청 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Posts.DoesNotExist:
            return Response({'message': '게시물을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
