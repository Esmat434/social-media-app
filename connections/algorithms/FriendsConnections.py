from django.contrib.auth import get_user_model
from django.db.models import Q,Count

User = get_user_model()

def shared_connections_suggestion(user,count=10):
    following_ids = user.following_connections.filter(status='accepted').values_list('to_user',flat=True)
    follower_ids = user.follower_connections.filter(status='accepted').values_list('from_user',flat=True)
    primary_connection_ids = set(list(following_ids)+list(follower_ids))

    if not primary_connection_ids:
        return User.objects.none()
    
    suggested_users = User.objects.filter(
        follower_connections__from_user_id__in=primary_connection_ids,
        follower_connections__status='accepted'
    )

    final_suggestions = suggested_users.exclude(
        Q(id=user.id) | Q(id__in=primary_connection_ids)
    )

    ranked_suggestions = final_suggestions.annotate(
        common_connections_count=Count(
            'follower_connections',
            filter=Q(follower_connections__from_user_id__in=primary_connection_ids)
        )
    ).order_by('-common_connections_count', '?')

    return ranked_suggestions.distinct().all()[:count]