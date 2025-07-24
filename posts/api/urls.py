from django.urls import path

from .views import (
    PostListCreateView,PostRetrieveDeleteUpdateView,CommentCreateView,CommentRetrieveUpdateDeleteView,
    LikeCreateView,LikeRetrieveDeleteView,ShareCreateView,ShareRetrieveDeleteView,SaveCreateView,
    SaveRetrieveDeleteView
)

urlpatterns = [
    path('post/create/',PostListCreateView.as_view(),name='post_create'),
    path('post/<int:pk>/',PostRetrieveDeleteUpdateView.as_view(),name='post_delete_or_update'),
    path('comment/create/',CommentCreateView.as_view(),name='comment_create'),
    path('comment/<int:pk>/',CommentRetrieveUpdateDeleteView.as_view(),name='comment_delete_or_update'),
    path('like/create/',LikeCreateView.as_view(),name='like_create'),
    path('like/<int:pk>/',LikeRetrieveDeleteView.as_view(),name='like_delete'),
    path('share/create/',ShareCreateView.as_view(),name='share_create'),
    path('share/<int:pk>/',ShareRetrieveDeleteView.as_view(),name='share_delete'),
    path('save/create/',SaveCreateView.as_view(),name='save_create'),
    path('save/<int:pk>/',SaveRetrieveDeleteView.as_view(),name='save_delete')
]