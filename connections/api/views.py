from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .permissions import CustomIsAuthenticated

from .serializers import (
    ConnectionSerializer
)

class ConnectionAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]
    
    def post(self,request):
        serializer = ConnectionSerializer(request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"success":"your connection was successfully."},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)