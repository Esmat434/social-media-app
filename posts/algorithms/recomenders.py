from django.db.models import Count,Q,F,Value,Case,When
from django.db.models.functions import Coalesce

from posts.models import Post

def get_recomended_posts(user):
    
    following = user.following.all()
    followers = user.followers.all()
    friends = following.intersection(followers)

    FRIEND_BONUS = 15
    LIKE_WEIGHT = 1
    COMMENT_WEIGHT = 3

    posts = Post.objects.filter(user__in=following)

    recomended_posts = posts.annotate(
        like_count=Coalesce(Count('likes', distinct=True), Value(0)),
        comment_count=Coalesce(Count('comments', distinct=True), Value(0)),
        is_friend_bonus=Case(
            When(user__in=friends, then=Value(FRIEND_BONUS)),
            default=Value(0)
        ),
        score=F('is_friend_bonus') + (F('like_count') * LIKE_WEIGHT) + (F('comment_count') * COMMENT_WEIGHT)
    ).order_by('-score','-created_at')

    return recomended_posts