# context_processors.py
from django.contrib.auth import get_user_model

User = get_user_model()

def is_user(request):
    username = request.resolver_match.kwargs.get('username') if request.resolver_match else None
    user = None
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
    return {'profile_user': user}
