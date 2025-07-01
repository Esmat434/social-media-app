from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class MaintenanceModeMiddleware(MiddlewareMixin):
    def __init__(self, get_response = ...):
        super().__init__(get_response)
        self.get_response = get_response
    
    def __call__(self, request):
        if (
            settings.MAINTENANCE_MODE
            and (not request.user.is_authenticated or not request.user.is_superuser)
        ):
            return render(request,'accounts/maintenance.html')
        response = self.get_response(request)
        return response