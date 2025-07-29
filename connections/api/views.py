from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import CustomIsAuthenticated
from django.db.models import Q 
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
            return Response({"success":"Your connection was successfull."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        
        to_user = get_object_or_404(User, username=username)
        from_user = request.user

        connection = Connection.objects.filter(from_user=from_user, to_user=to_user)
        
        if connection.exists():
            connection.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({"error": "You are not following this user."}, status=status.HTTP_404_NOT_FOUND)

class UserPrivateToggleAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]

    def post(self,request,username):
        from_user = request.user
        to_user = get_object_or_404(User, username=username)

        if from_user == to_user:
            return Response({'error':"You cannot connect to yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        if Connection.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'error':"This connection already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        Connection.objects.create(
                from_user=from_user, 
                to_user=to_user, 
                status=Connection.ConnectionStatus.PENDING
            )
        
        return Response({"success":"your connection successfully created."}, status=status.HTTP_201_CREATED)
    
    def put(self,request,username):
        from_user = get_object_or_404(User, username=username)
        to_user = request.user

        connection = get_object_or_404(
            Connection,
            from_user=from_user,
            to_user=to_user,
            status = Connection.ConnectionStatus.PENDING
        )

        connection.status = Connection.ConnectionStatus.ACCEPTED
        connection.save()

        Connection.objects.create(
            from_user=to_user,
            to_user=from_user,
            status=Connection.ConnectionStatus.ACCEPTED
        )

        return Response({"success":"The connection request has been accepted."}, status=status.HTTP_200_OK)

    def delete(self,request,username):
        user1 = request.user
        user2 = get_object_or_404(User, username=username)

        connection_request = Connection.objects.filter(
            (Q(from_user=user1,to_user=user2) | Q(from_user=user2,to_user=user1)),
            status=Connection.ConnectionStatus.PENDING
        ).first()

        if not connection_request:
            return Response({"error":"No pending request found."}, status=status.HTTP_400_BAD_REQUEST)
        
        connection_request.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)