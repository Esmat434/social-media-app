from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth import get_user_model

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
        if request.user.is_authenticated:
            connections = Connection.objects.filter(
                (
                    Q(to_user=request.user) | Q(from_user=request.user)
                ) & (
                    Q(status=Connection.ConnectionStatus.ACCEPTED) | Q(status=Connection.ConnectionStatus.PENDING)
                )
            )

            from_user_ids = connections.values_list('from_user', flat=True)
            to_user_ids = connections.values_list('to_user', flat=True)
            return from_user_ids, to_user_ids
        return [],[]
    
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

        from_user_ids,to_user_ids = self.get_connected_ids(request)

        near_network_ids = near_network_list.values_list('id', flat=True)
        
        other_network_list = User.objects.exclude(
            Q(id__in=near_network_ids) |
            Q(id__in=from_user_ids) |
            Q(id__in=to_user_ids)
        )

        return other_network_list
    
    def get_connection_count(self,request):
        if request.user.is_authenticated:
            return Connection.objects.filter(
                (
                    Q(from_user=request.user) | Q(to_user=request.user)
                ) & (
                    Q(status=Connection.ConnectionStatus.ACCEPTED)
                )
            ).count()
        return 0
    
    def get_follower_count(self,request):
        if request.user.is_authenticated:
            return Connection.objects.filter(
                to_user = request.user,
                status = Connection.ConnectionStatus.ACCEPTED
            ).count()
        return 0

class NotificationListView(View):
    def get(self,request):
        
        context = {
            'notifications':self.get_notifications(request),
            'notification_count':self.get_notification_count(request)
        }
        
        return render(request,'home/notification.html',context=context)
    
    def get_notifications(self, request):
        if request.user.is_authenticated:
            notifications = Notification.objects.filter(recipient=request.user)
            return notifications
        return Notification.objects.none()
    
    def get_notification_count(self, request):
        if request.user.is_authenticated:
            notification_count = Notification.objects.filter(recipient=request.user).count()
            return notification_count
        return 0

class SaveListView(LoginRequiredMixin,View):
    def get(self,request):
        post_save = Save.objects.filter(user=request.user)

        context = {
            'posts':post_save
        }
        return render(request,'home/post_save.html',context=context)