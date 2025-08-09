from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from watson import search as watson_search

from posts.models import (
    Post
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
        query = request.GET.get('q', '')
        results = []
        if query:
            user_results = watson_search.filter(User,query)
            results = user_results
        print(query)
        context = {
            'other_network_list': results,
            'near_network_list': []
        }

        return render(request,'home/network.html', context=context)

class SearchNotificationView(View):
    def get(self,request):
        query = request.GET.get('q', '')
        results = []
        if query:
            notification_results = watson_search.filter(Notification,query)
            results = notification_results
        
        context = {
            'notifications': results
        }

        return render(request,'home/notification.html', context=context)