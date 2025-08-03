from django import template

from connections.models import (
    Connection
)

register = template.Library()

@register.filter
def is_connected(user1,user2):
    return Connection.objects.filter(
        from_user=user1, to_user=user2, status='accepted'
    ).exists() or Connection.objects.filter(
        from_user=user2, to_user=user1, status='accepted'
    ).exists()

@register.filter
def is_pending(user1,user2):
    return Connection.objects.filter(
        from_user=user1, to_user=user2, status='pending'
    ).exists() or Connection.objects.filter(
        from_user=user2, to_user=user1, status='pending'
    ).exists()