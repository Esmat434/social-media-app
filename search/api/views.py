from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q
from itertools import chain
from watson import search as watson_search

from posts.models import (
    Post, Save
)
from posts.api.serializers import (
    PostSerializer,SaveSerializer
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

class SearchPostSaveView(APIView):
    def get(self, request):

        post_save = self.get_post_save(request)
        serializer = SaveSerializer(post_save, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_posts(self, request):
        query = request.GET.get('q','')
        if not query:
            return []
        
        watson_result = watson_search.filter(Post, query)
        watson_result_ids = watson_result.values_list('id', flat=True)

        partial_result_ids = Post.objects.filter(
            content__icontains=query
        ).exclude(id__in=watson_result_ids).values_list('id', flat=True)

        results = list(chain(watson_result_ids,partial_result_ids))

        return results
    
    def get_post_save(self, request):
        if not request.user.is_authenticated:
            return []
        
        post_ids = self.get_posts(request)

        post_save = Save.objects.filter(
            post__in=post_ids,
            user=request.user
        )

        return post_save
    
class SearchFriendView(APIView):
    def get(self,request):
        
        users = self.get_users(request)
        serializers = UserSerializer(users, many=True)

        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def get_all_connection(self, request):
        connection_ids = Connection.objects.filter(
            Q(from_user=request.user) |
            Q(to_user=request.user),
            status=Connection.ConnectionStatus.ACCEPTED
        ).values_list('from_user', 'to_user')

        result = set()
        for from_user,to_user in connection_ids:
            if from_user != request.user.id:
                result.add(from_user)
            if to_user != request.user.id:
                result.add(to_user)
        
        return result

    def get_users(self,request):
        query = request.query_params.get('q', '')
        if not query:
            return []
        
        connection_ids = self.get_all_connection(request)        
        
        watson_result = watson_search.filter(User, query).filter(
            id__in=connection_ids
        )
        watson_result_ids = set(watson_result.values_list('id', flat=True))
        
        partial_result = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query),
                id__in=connection_ids, 
            ).exclude(id__in=watson_result_ids)
        
        result = list(chain(watson_result, partial_result))

        return result