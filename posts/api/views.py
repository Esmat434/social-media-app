from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    PostSerializer,CommentSerializer,LikeSerializer,ShareSerializer,SaveSerializer
)

from posts.models import (
    Post,Comment,Like,Share,Save
)

class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostRetrieveDeleteUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        post = get_object_or_404(Post, id=pk)

        serializer = PostSerializer(post)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,pk):
        post = get_object_or_404(Post, id=pk, user=request.user)
        
        serializer = PostSerializer(instance=post ,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        post = get_object_or_404(Post, id=pk, user=request.user)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        comment = get_object_or_404(Comment, id=pk, user=request.user)
        serializer = CommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,pk):
        comment = get_object_or_404(Comment, id=pk, user=request.user)
        serializer = CommentSerializer(instance=comment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        comment = get_object_or_404(Comment, id=pk, user=request.user)
        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class LikeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeRetrieveDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        like = get_object_or_404(Like, id=pk, user=request.user)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,pk):
        like = get_object_or_404(Like, id=pk, user=request.user)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShareCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serialzier = ShareSerializer(data=request.data)
        if serialzier.is_valid():
            serialzier.save(user=request.user)
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)

class ShareRetrieveDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        share = get_object_or_404(Share, id=pk, user=request.user)
        serializer = ShareSerializer(share)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,pk):
        share = get_object_or_404(Share, id=pk, user=request.user)
        share.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SaveCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = SaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaveRetrieveDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        save = get_object_or_404(Save, id=pk, user=request.user)
        serializer = SaveSerializer(save)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,pk):
        save = get_object_or_404(Save, id=pk, user=request.user)
        save.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

