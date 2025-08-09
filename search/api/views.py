from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from watson import search as watson_search

from posts.models import (
    Post
)
from posts.api.serializers import (
    PostSerializer
)

from accounts.api.serializers import (
    UserSerializer
)

User = get_user_model()

class SearchPostView(APIView):
    def get(self,request):
        query = request.query_params.get('q')
        results = []
        if query:
            post_results = watson_search.filter(Post,query)
            results = [result.object for result in post_results]
        
        serializers = PostSerializer(results, many=True)
        return Response(serializers.data, status=200)

class SearchUserView(APIView):
    def get(self,request):
        query = request.query_params.get('q')
        results = []
        if query:
            user_result = watson_search.filter(User,query)
            results = [result.object for result in user_result]
        
        serializers = UserSerializer(results, many=True)
        return Response(serializers.data, status=200)