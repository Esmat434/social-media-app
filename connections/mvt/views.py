from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model

from .mixins import (
    CustomLoginRequiredMixin
)

from connections.models import Connection

User = get_user_model()

class ConnectionView(CustomLoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        self.user_id = kwargs['pk']
        self.user_instance = get_object_or_404(User, id=self.user_id)

        return super().dispatch(request,*args,**kwargs)

    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user = self.user_instance

        if Connection.objects.filter(from_user=from_user, to_user=to_user).exists():
            return JsonResponse({"error": "Connection already exists."}, status=400)
        
        Connection.objects.create(from_user=from_user, to_user=to_user)
        return JsonResponse({"success":"Connection created successfully."},status=201)