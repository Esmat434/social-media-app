from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import CustomIsAuthenticated 
from django.contrib.auth import get_user_model
from connections.models import Connection
from .serializers import ConnectionSerializer
from django.shortcuts import get_object_or_404

User = get_user_model()

class FollowToggleAPIView(APIView):
    
    permission_classes = [CustomIsAuthenticated]

    def post(self, request, username):
        
        to_user = get_object_or_404(User, username=username)
        from_user = request.user

        
        data = {'to_user': to_user.pk}
        serializer = ConnectionSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save(from_user=from_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        
        to_user = get_object_or_404(User, username=username)
        from_user = request.user

        connection = Connection.objects.filter(from_user=from_user, to_user=to_user)
        
        if connection.exists():
            connection.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({"error": "You are not following this user."}, status=status.HTTP_404_NOT_FOUND)