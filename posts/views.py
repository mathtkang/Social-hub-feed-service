
from .models import Posts
from accounts.models import User
from .serializers import PostSerializer, PostsStatisicsDetailSerializer
from rest_framework import generics, status, filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from itertools import product
from django.shortcuts import render
from django.conf import settings

from django.db.models import Q
from datetime import datetime, timedelta


from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from posts.models import Posts, HashTags
from posts.serializers import PostSerializer

import traceback
import jwt 

from collections import defaultdict
# token을 decode하기 위해서는 두가지가 필요
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'


# Blog의 detail을 보여주는 역할
class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    
    # permission_classes = [IsAuthenticated, ]
    permission_classes = [AllowAny, ]
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = get_object_or_404(Posts, id=pk)
        # #Posts에서 가지고온 query에서 해당 게시물 조회수를 가지고 옵니다.
        # view_count = self.queryset.values().get(id=pk)['view_count']
        #get요청이 들어 올때 마다 해달 view_count를 +1합니다.
        instance.view_count += 1
        instance.save()
        
        return self.retrieve(request, *args, **kwargs)

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
    
# 해당 View는 자신이 테그 되어 있거나 원하는 hashtag를 함으로써 해당 hastag에 대한 인기도 즉, 얼마나 공유되었는지, 얼마나 조회했는지, 얼마나 많은 사람들이 좋아요를 눌렀는지 알수 있습니다.
# 추후 전체적인 인기 hashtag나 게시글에 많이 작성되는 단어등을 순위로 보여주는 기능도 있으면 좋을 것 같습니다. 
#해당 뷰는 value와 type에 따라 조회 할 수 있는 수가 달라집니다.
#type이 date일때는 30일 hour일때는 7일로 제한을 두었습니다. 
#해당 기간 동안 일 또는 시간 단위로 적용되는 죄회수를 알 수 있습니다.
class PostsStatisicsDetailView(APIView):
    #jwt 인증 할때 사용하는 인증 방식입니다.
    permission_classes=[IsAuthenticated]
    
    
    queryset = Posts.objects.all()
    
    #get의 parameter를 통해 value값과 type값에 따라 return 되는 값을 달리 합니다.
    def get(self, request):
        # token으로 부터 user_id를 가지고 옵니다.
        # header로 넘어온 token에서 user_id값을 가지고 옵니다.
        token_str = request.headers.get("Authorization").split(' ')[1]
        data = jwt.decode(token_str, SECRET_KEY, ALGORITHM)
        instance = get_object_or_404(User, id=data['user_id'])
        user_id = instance.username
        
        query_params = self.request.query_params
        #hashtag or 원하는 값에 대한 통계
        hashtag = query_params.get('hashtag', user_id)
        #value값은 어떤값의 합을 제공할 것인가, default는 count
        value = query_params.get('value', 'count')
        
        # start와 end에 들어가야하는 값은 7일전 날짜와 오늘 날짜와 시간입니다.
        # 오늘의 날짜를 가져옵니다
        today = datetime.today()
        # 7일 전의 날짜를 계산합니다
        seven_days_ago = today - timedelta(days=7)
        
        #어떤 type인지 지정 default는 date
        type = query_params.get('type', 'date')
        #type이 date일때는 start와 end의 값이 '2023-10-0'이러한 형태로 들어와야 한다.
        if type == 'date':
            start = datetime.strptime(query_params.get('start', seven_days_ago.strftime('%Y-%m-%d')), '%Y-%m-%d')
            end = datetime.strptime(query_params.get('end', today.strftime('%Y-%m-%d')), '%Y-%m-%d')
            
            date_difference = end - start
            #날짜 차이가 30일 이상일 경울 기간 단위를 30일로 하라고 알려줘야함
            if date_difference.days <= 30:
                total, count_dict = self.count_of_date(value, hashtag, start, end, type)
            else:
                return Response({"error": "기간이 30일 이하로 설정되어야 합니다."}, status=status.HTTP_400_BAD_REQUEST)
        #tpye이 hour일때는 start와 end의 값이 '2023-10-01 00:00' 이러한 형태로 들어와야 한다.
        else:
            start = datetime.strptime(query_params.get('start', seven_days_ago.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(query_params.get('end', today.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
            
            date_difference = end - start
            #날짜 차이가 7일 이상인 경우 기간 단위를 7일 이내로 하라고 알려줘야합니다.
            if date_difference.days <= 7:
                    total, count_dict = self.count_of_date(value, hashtag, start, end, type)
            else:
                return Response({"error": "기간이 7일 이하로 설정되어야 합니다."}, status=status.HTTP_400_BAD_REQUEST)
       
        # 보내고자하는 data serialize
        serializer = PostsStatisicsDetailSerializer(data={'total': total, 'count_dict': count_dict})
        
        
        if serializer.is_valid(raise_exception=True):
            serialized_data = serializer.data
            response = Response(data=serialized_data)
            response.headers['Content-Type'] = 'application/json'
            try:
                return response
            except:
                traceback.print_exc() 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def date_range(self, start, end):
        #시간 간격을 일 단위로 생성
        dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
        return dates
    
    def hour_range(self, start, end):
        # 시간 간격을 시간 단위로 생성
        time_intervals = [(start + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(int((end-start).total_seconds() / 3600) + 1)]
        return time_intervals
    
    def count_of_date(self, value, hashtag, start, end, type):
        counts = defaultdict(int)
        total = 0
        
        if type == 'date':
            date_data = self.date_range(start, end)
        else:
            date_data = self.hour_range(start, end)
            
        if value == 'count':
            #해당 hashtag가 있는 모든 query를 가지고 옵니다.
            queryset = self.queryset.filter(content__icontains='#' + hashtag)
            # 일단 위로 가지고온 조회수의 합을 구하기 위해 일단위 date_list를 만듭니다.
            
            total = 0
            for s, e in zip(date_data[:-1], date_data[1:]):
                #필터를 적용할 때 해당 열값 또는 field값에 __gt를 붙이면 초과 __lt를 붙이면 미만인 값을 return 합니다
                data_within_range = queryset.filter(created_at=s, created_at__lt=e)
                
                cnt = data_within_range.count()
                counts[s] = cnt
                total += cnt
        else:
            #해당 hashtag가 있는 모든 query를 가지고 옵니다.
            queryset = self.queryset.filter(content__icontains='#' + hashtag)
            # 일단 위로 가지고온 조회수의 합을 구하기 위해 일단위 date_list를 만듭니다.
            total = 0
            for s, e in zip(date_data[:-1], date_data[1:]):
                
                data_within_range = queryset.filter(created_at=s, created_at__lt=e)
                
                if data_within_range:
                    for obj in data_within_range.values():
                        counts[s] += obj[value]
                        total += obj[value]
                else:
                    counts[s] = 0
                    
        return total, counts
    
    