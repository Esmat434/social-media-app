from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import transaction
from django.views.generic import (
    CreateView,UpdateView,DeleteView,View
)

from .mixins import (
    CustomLoginRequiredMixin
)

from posts.models import (
    Post,Like,Comment,Share,Save
)

from .forms import (
    PostForm,PostMediaForm,CommentForm
)

class CreatePostView(CustomLoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'
    context_object_name = 'form'
    success_url = '/'

    def form_valid(self, form):
        with transaction.atomic():
            post = form.save(commit=False)
            post.user = self.request.user
            post.save()

            if self.request.FILES:
                media_form = PostMediaForm(files=self.request.FILES)
                if media_form.is_valid():
                    media = media_form.save(commit=False)
                    media.post = post
                    media.save()
                else:
                    form.add_error(None,'Media form is not valid.')

        return super().form_valid(form)

class EditPostView(CustomLoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_edit.html'
    context_object_name = 'form'
    success_url = '/'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class DeletePostView(CustomLoginRequiredMixin,DeleteView):
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('mvt:profile', kwargs={'username':self.request.user.username})

class CreateCommentView(CustomLoginRequiredMixin,View):

    def post(self,request,pk):
        post = get_object_or_404(Post, id=pk)

        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return JsonResponse({'success':'comment successfully sended.'},status=201)
        else:
            return JsonResponse({'error':'comment does not send.'},status=400)

class CreateParentCommentView(CustomLoginRequiredMixin,View):

    def post(self,request,post_pk,comment_pk):
        post = get_object_or_404(Post, id=post_pk)
        parent_comment = get_object_or_404(Comment, id=comment_pk)

        form = CommentForm(data=request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.parent = parent_comment
            comment.save()
            return JsonResponse({'success':'Your comment successfully sended.'},status=201)
        else:
            return JsonResponse({'error':'Your comment does not sended.'},status=400)

class EditCommentView(CustomLoginRequiredMixin,View):

    def post(self,request,pk):
        comment = get_object_or_404(Comment, id=pk, user=request.user)
        form = CommentForm(data=request.POST,instance=comment)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success':'data edited.'},status=200)
        else:
            return JsonResponse({'error':'data was invalid.'},status=400)

class DeleteCommentView(CustomLoginRequiredMixin,View):

    def post(self,request,pk):
        comment = get_object_or_404(Comment, id=pk, user=request.user)
        comment.delete()
        return JsonResponse({'succes':'data successfully deleted.'},status=204)

class CreateLikeView(CustomLoginRequiredMixin,View):
    
    def post(self,request,pk):
        post = get_object_or_404(Post, id=pk)

        like = Like.objects.filter(user=request.user,post=post)
        if like.exists():
            like.delete()
            return JsonResponse({'success':'unlike'},status=204)
        else:
            Like.objects.create(user=request.user,post=post)

        return JsonResponse({'success':'like'},status=201)

class CreateShareView(CustomLoginRequiredMixin,View):

    def post(self,request,pk):
        post = get_object_or_404(Post, id=pk)

        share = Share.objects.filter(user=request.user, post=post)
        if share.exists():
            share.delete()
            return JsonResponse({'success':'unshare'},status=204)
        else:
            Share.objects.create(user=request.user, post=post)
        
        return JsonResponse({'success':'share'},status=201)

class CreateSaveView(CustomLoginRequiredMixin,View):

    def post(self,request,pk):
        post = get_object_or_404(Post, id=pk)

        save = Save.objects.filter(user=request.user, post=post)
        if save.exists():
            save.delete()
            return JsonResponse({'success':'unsave'},status=204)
        else:
            Save.objects.create(user=request.user, post=post)
        
        return JsonResponse({'success':'save'},status=201)
