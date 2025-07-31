from django.shortcuts import render,get_object_or_404
from django.views import View

from connections.models import (
    Connection
)
from connections.algorithms.FriendsConnections import (
    shared_connections_suggestion
)

from posts.models import (
    Post
)
from posts.algorithms.recomenders import (
    get_recomended_posts
)

class PostListView(View):
    def get(self,request):
        best_posts = []
        if request.user.is_authenticated:
            best_posts = get_recomended_posts(request.user)

        best_post_ids = best_posts.values_list('id', flat=True)
        other_posts = Post.objects.exclude(id__in=best_post_ids).order_by('-created_at')

        context = {
            'best_posts':best_posts,
            'other_posts':other_posts
        }

        return render(request,'home/home.html',context=context)

class NetworkListView(View):
    def get(self,request):
        near_network_list = []
        invitation_list = []
        if request.user.is_authenticated:
            invitation_list = Connection.objects.filter(to_user=request.user, status=Connection.ConnectionStatus.PENDING)
            near_network_list = shared_connections_suggestion(request.user)

        near_network_ids = near_network_list.values_list('id', flat=True)
        other_network_list = Connection.objects.exclude(id__in=near_network_ids)

        context = {
            'invitation_list':invitation_list,
            'near_network_list':near_network_list,
            'other_network_list':other_network_list
        }

        return render(request,'home/network.html',context=context)

