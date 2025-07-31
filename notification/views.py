from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Notification
# Create your views here.

class DeleteNotificatoinView(LoginRequiredMixin,View):
    def post(self,request, pk):
        notification = get_object_or_404(
            Notification, 
            id=pk,
            recipient = request.user
        )

        target_url = None
        if notification.target and hasattr(notification.target, 'get_absolute_url'):
            target_url = notification.target.get_absolute_url()
        
        notification.delete()

        if target_url:
            return redirect(target_url)
        
        return redirect('home:home-feed')
    