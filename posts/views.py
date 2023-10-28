from itertools import product
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db.models import Q

from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from posts.models import Posts, HashTags
from posts.serializers import PostSerializer

## constants
ORDER_BY = [s+o for s, o in list(product(['-', ''],['created_at', 'updated_at','like_count','share_count', 'view_count']))]


class PostsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class SearchPostsList(ListAPIView):
    # permission_classes = [IsAuthenticated, ]
    permission_classes = [AllowAny, ]
    
    serializer_class = PostSerializer
    pagination_class = PostsPagination
    
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = Posts.objects.all()

        # hashtag, type, order_by, search_by, search 파라미터 처리
        query_params = self.request.query_params
        hashtag = query_params.get('hashtag', self.request.user.username)
        if hashtag:
            queryset = queryset.filter(content__icontains='#'+hashtag)
        # if hashtag:
        #     queryset = queryset.filter(hashtags__name__exact=hashtag)

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
        # else:
        #     raise ValueError(f'쿼리 파라미터 "search"의 값이 필요합니다.')

        return queryset