
from rest_framework import serializers

from posts.models import Posts, HashTags


class PostSerializer(serializers.ModelSerializer):
    class Meta():
        model = Posts
        fields = '__all__'


class HashTagSerializer(serializers.ModelSerializer):
    class Meta():
        model = HashTags
        fields = '__all__'
        
class PostsStatisicsDetailSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    count_dict = serializers.DictField(child=serializers.IntegerField(), allow_empty=True)