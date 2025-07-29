from django.shortcuts import get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.views import View
from django.contrib.auth import get_user_model

from .mixins import (
    CustomLoginRequiredMixin
)

from connections.models import Connection

User = get_user_model()

class FollowView(CustomLoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        self.user_name = kwargs['username']
        self.user_instance = get_object_or_404(User, username=self.user_name)

        return super().dispatch(request,*args,**kwargs)

    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user = self.user_instance

        if from_user == to_user:
            return JsonResponse({"error":"You cannot connect to yourself."}, status=400)

        if Connection.objects.filter(from_user=from_user, to_user=to_user).exists():
            return JsonResponse({"error": "Connection already exists."}, status=400)
        
        Connection.objects.create(from_user=from_user, to_user=to_user,status=Connection.ConnectionStatus.PENDING)
        return JsonResponse({"success":"Connection created successfully."},status=201)

class UserPrivateRequestView(CustomLoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        username = kwargs['username']
        self.user_instance = get_object_or_404(User, username=username)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request,*args,**kwargs):
        from_user = request.user
        to_user = self.user_instance

        if from_user == to_user:
            return JsonResponse({'error':'You cannot send request to yourself.'}, status=400)
        
        if Connection.objects.filter(from_user=from_user, to_user=to_user).exists():
            return JsonResponse({'error':'This connected already exists.'}, status=400)
        
        Connection.objects.create(from_user=from_user, to_user=to_user)
        return JsonResponse({'success':'Your connection successfully created.'}, status=201)
    
class UserPrivateAcceptRequestView(CustomLoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        username = kwargs['username']
        self.user_instance = get_object_or_404(User, username=username)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        from_user = self.user_instance
        to_user = request.user

        connection = get_object_or_404(Connection, from_user=from_user, to_user=to_user, status=Connection.ConnectionStatus.PENDING)
        connection.status = Connection.ConnectionStatus.ACCEPTED
        connection.save()

        Connection.objects.update_or_create(
            from_user=to_user,
            to_user=from_user,
            defaults={'status': Connection.ConnectionStatus.ACCEPTED}
        )

        return JsonResponse({"success":"Your connection is accepted."}, status=200)

class UserPrivateRejectRequestView(CustomLoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        username = kwargs['username']
        self.user_instance = get_object_or_404(User, username=username)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request,*args,**kwargs):
            from_user = request.user
            to_user = self.user_instance

            connection = get_object_or_404(
                    Connection, 
                    from_user=to_user, 
                    to_user=from_user, 
                    status=Connection.ConnectionStatus.PENDING
                )
            connection.delete()

            return HttpResponse(status=204)

class UnFollowView(CustomLoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        username = kwargs['username']
        self.user_instance = get_object_or_404(User, username=username)

        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request, *args, **kwargs):
        from_user = request.user
        to_user = self.user_instance

        connection = get_object_or_404(Connection, from_user=from_user, to_user=to_user, status=Connection.ConnectionStatus.ACCEPTED)
        
        connection.delete()
        
        Connection.objects.filter(from_user=to_user, to_user=from_user, status=Connection.ConnectionStatus.ACCEPTED).delete()

        return HttpResponse(status=204)