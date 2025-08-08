from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            recipient=request.user,
        ).count()
    else:
        count = 0
    
    return {
        'notification_count':count
    }