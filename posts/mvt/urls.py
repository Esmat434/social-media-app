from django.urls import path

from .views import (
    CreatePostView,EditPostView,DeletePostView,CreateCommentView,CreateParentCommentView,
    EditCommentView,DeleteCommentView,CreateLikeView,CreateShareView,CreateSaveView
)

urlpatterns = [
    path('post/create/',CreatePostView.as_view(),name='create_post'),
    path('post/<int:pk>/edit/',EditPostView.as_view(),name='edit_post'),
    path('post/<int:pk>/delete/',DeletePostView.as_view(),name='delete_post'),
    path('comment/<int:pk>/create/',CreateCommentView.as_view(),name='create_comment'),
    path('parent_comment/<int:post_pk>/<int:comment_pk>/create/',CreateParentCommentView.as_view(),name='create_parent_comment'),
    path('comment/<int:pk>/edit/',EditCommentView.as_view(),name='edit_comment'),
    path('comment/<int:pk>/delete/',DeleteCommentView.as_view(),name='delete_comment'),
    path('like/<int:pk>/create/',CreateLikeView.as_view(),name='create_like'),
    path('share/<int:pk>/create/',CreateShareView.as_view(),name='create_share'),
    path('save/<int:pk>/create/',CreateSaveView.as_view(),name='create_save')
]