from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model

from .mixins import (
    CustomLoginRequiredMixin
)

from connections.models import (
    Connection
)
from connections.algorithms.FriendsConnections import (
    shared_connections_suggestion
)

from posts.models import (
    Post,Save
)
from posts.mvt.forms import (
    CommentForm
)
from posts.algorithms.recomenders import (
    get_recomended_posts
)

from notification.models import (
    Notification
)

User = get_user_model()

class PostListView(View):
    def get(self,request):
        best_posts = []
        if request.user.is_authenticated:
            best_posts = get_recomended_posts(request.user)

        best_post_ids = [post.id for post in best_posts]
        other_posts = Post.objects.exclude(id__in=best_post_ids).order_by('-created_at')

        context = {
            'best_posts':best_posts,
            'other_posts':other_posts,
            'comment_form':CommentForm()
        }

        return render(request,'home/home.html',context=context)

class NetworkListView(View):
    def get(self,request):

        context = {
            'invitation_list':self.get_invitation_users(request),
            'near_network_list':self.get_near_network_users(request),
            'other_network_list':self.get_other_network_users(request),
            'connection_count':self.get_connection_count(request),
            'follower_count':self.get_follower_count(request)
        }

        return render(request,'home/network.html',context=context)

    def get_connected_ids(self,request):
        if not request.user.is_authenticated:
            return set()
        
        connections = Connection.objects.filter(
            (
                Q(to_user=request.user) | Q(from_user=request.user)
            ) & (
                Q(status=Connection.ConnectionStatus.ACCEPTED) | Q(status=Connection.ConnectionStatus.PENDING)
            )
        ).values_list('from_user','to_user')
        
        connected_ids = set()

        for from_user,to_user in connections:
            if from_user != request.user.id:
                connected_ids.add(from_user)
            if to_user != request.user.id:
                connected_ids.add(to_user)
        
        return connected_ids
    
    def get_invitation_users(self,request):
        if request.user.is_authenticated:
            return Connection.objects.filter(to_user=request.user, status=Connection.ConnectionStatus.PENDING)
        return []
    
    def get_near_network_users(self,request):
        if request.user.is_authenticated:
            return shared_connections_suggestion(request.user)
        return User.objects.none()
    
    def get_other_network_users(self,request):
        near_network_list = self.get_near_network_users(request)

        connected_ids = self.get_connected_ids(request)

        near_network_ids = near_network_list.values_list('id', flat=True)
        
        # Combine all IDs to be excluded
        exclude_ids = set(near_network_ids) | connected_ids
        
        other_network_list = User.objects.exclude(
            # Exclude users in near network, existing connections, AND the user themselves
            Q(id__in=exclude_ids) | Q(id=request.user.id)
        )

        return other_network_list
    
    def get_connection_count(self,request):
        if not request.user.is_authenticated:
            return 0
        friends = Connection.objects.filter(
            (
                Q(from_user=request.user) | Q(to_user=request.user)
            ), 
            status=Connection.ConnectionStatus.ACCEPTED
        ).values_list('from_user','to_user')

        friend_ids = set()
        for f1,f2 in friends:
            friend_ids.add(f1 if f1 != request.user.id else f2)
        count = len(friend_ids)
        return count
    
    def get_follower_count(self,request):
        if request.user.is_authenticated:
            return Connection.objects.filter(
                    to_user=request.user,
                    status=Connection.ConnectionStatus.ACCEPTED
                ).count()
        return 0

class NotificationListView(View):
    def get(self,request):
        
        context = {
            'notifications':self.get_notifications(request)
        }
        
        return render(request,'home/notification.html',context=context)
    
    def get_notifications(self, request):
        if request.user.is_authenticated:
            notifications = Notification.objects.filter(recipient=request.user)
            return notifications
        return Notification.objects.none()

class SaveListView(CustomLoginRequiredMixin,View):
    def get(self,request):

        context = {
            'posts':self.get_post_save(request)
        }
        
        return render(request,'home/post_save.html',context=context)
    
    def get_post_save(self, request):
        if not request.user.is_authenticated:
            return []
        
        return Save.objects.filter(
            user=request.user
        )