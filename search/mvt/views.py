from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.contrib.auth import get_user_model
from watson import search as watson_search
from itertools import chain

from posts.models import (
    Post,Save
)

from connections.models import (
    Connection
)

from notification.models import (
    Notification
)

User = get_user_model()

class SearchPostView(View):
    def get(self,request):
        query = request.GET.get('q', '')
        results = []
        if query:
            post_results = watson_search.filter(Post,query)
            results = post_results
        
        context = {
            'other_posts': results,
            'best_posts': []
        }

        return render(request,'home/home.html', context=context)

class SearchNetworkView(View):
    def get(self,request):
        
        context = {
            'other_network_list': self.get_search_results(request),
            'near_network_list': []
        }

        return render(request,'home/network.html', context=context)

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
        query = request.GET.get('q', '')
        if not query:
            return []

        connected_user_ids = self.get_connected_users_id(request)
        
        # همیشه ID کاربر فعلی را هم به لیست استثنائات اضافه کن
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

class SearchNotificationView(View):
    def get(self,request):
        
        context = {
            'notifications': self.get_results(request) 
        }

        return render(request,'home/notification.html', context=context)
    
    def get_my_notification_ids(self,request):
        if not request.user.is_authenticated:
            return []
        
        return Notification.objects.filter(
            recipient=request.user
        ).values_list('id', flat=True)

    def get_results(self,request):
        query = request.GET.get('q', '')
        my_notification_ids = self.get_my_notification_ids(request)
        if not query:
            return []
        
        notification_results = watson_search.filter(Notification,query)
        watson_results = notification_results.filter(id__in=my_notification_ids)
        
        partial_results = Notification.objects.filter(
            verb__icontains=query
        ).exclude(
            id__in=[result.id for result in watson_results]
        )

        results = list(chain(partial_results, watson_results))

        return results
    
class SearchPostSaveView(View):
    def get(self, request):

        context = {
            'posts':self.get_post_save(request)
        }

        return render(request,'home/post_save.html', context=context)
    
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