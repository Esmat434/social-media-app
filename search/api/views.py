from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q
from itertools import chain
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

from connections.models import (
    Connection
)

User = get_user_model()

class SearchPostView(APIView):
    def get(self,request):
        query = request.query_params.get('q')
        if not query:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        post_results = watson_search.filter(Post,query)
        results = post_results
        
        serializers = PostSerializer(results, many=True)
        return Response(serializers.data, status=200)

class SearchUserView(APIView):
    def get(self,request):
        results = self.get_search_results(request)
        serializers = UserSerializer(results, many=True)
        return Response(serializers.data, status=200)
    
    def get_connected_users_id(self,request):
        if not request.user.is_authenticated:
            return [] 
        
        connections = Connection.objects.filter(
            (Q(from_user=request.user) | Q(to_user=request.user)),
            (Q(status=Connection.ConnectionStatus.ACCEPTED) | Q(status=Connection.ConnectionStatus.PENDING))
        )
        
        connected_ids = set()
        for conn in connections:
            if conn.from_user_id != request.user.id:
                connected_ids.add(conn.from_user_id)
            if conn.to_user_id != request.user.id:
                connected_ids.add(conn.to_user_id)
        
        return list(connected_ids)
    
    def get_search_results(self,request):
        query = request.query_params.get('q', '')
        if not query:
            return []

        connected_user_ids = self.get_connected_users_id(request)
        
        all_excluded_ids = set(connected_user_ids)
        if request.user.is_authenticated:
            all_excluded_ids.add(request.user.id)
        
        watson_results = watson_search.filter(User,query)
        watson_results=watson_results.exclude(id__in=connected_user_ids)
        watson_results_ids = [result.id for result in watson_results]
        all_excluded_ids = list(all_excluded_ids)+watson_results_ids

        partial_results = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(
            id__in=all_excluded_ids
        )

        results = list(chain(watson_results, partial_results))

        return results