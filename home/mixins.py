from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin

class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self ,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('mvt:login')
        return super().dispatch(request, *args, **kwargs)