from django import template

from posts.models import (
    Save,Share,Like
)

register = template.Library()

@register.filter
def is_saved(post,user):
    return Save.objects.filter(
        user=user,
        post=post
    ).exists()

@register.filter
def is_shared(post,user):
    return Share.objects.filter(
        user=user,
        post=post
    ).exists()

@register.filter
def is_liked(post,user):
    return Like.objects.filter(
        user=user,
        post=post
    ).exists()