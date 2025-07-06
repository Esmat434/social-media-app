from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .permissions import (
    isAuthenticatedCustom,isNotAuthenticatedCustom
)

from accounts.models import (
    CustomUser
)

from .serializers import (
    UserSerializer,UpdateUserSerializer,LoginSerializer,ChangePasswordSerializer,
    ForgotPasswordSerializer
)

class RegisterAPIView(APIView):
    permission_classes = [isNotAuthenticatedCustom]

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.email_verified=True
            user.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    

class LoginAPIView(APIView):
    permission_classes = [isNotAuthenticatedCustom]

    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request,user)
                return Response({'success':'You successfully Logged In.'},status=status.HTTP_200_OK)    
            return Response({"error":"Your username or password is incorrect."},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [isAuthenticatedCustom]

    def post(self,request):
        
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error":"Refresh Token is required."},status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            logout(request)
            return Response({"msg":'Your successfully Logged Out.'},status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error":"Invalid or expired token."},status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):
    permission_classes = [isAuthenticatedCustom]

    def get(self,request,pk):
        user = get_object_or_404(CustomUser,id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProfileUpdateAPIView(APIView):
    def put(self,request,pk):
        user = get_object_or_404(CustomUser,id=pk)
        serializer = ProfileUpdateAPIView(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(APIView):
    permission_classes = [isAuthenticatedCustom]
    
    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request.user)
            return Response({'msg':'Your password successfully changed.'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordAPIView(APIView):
    permission_classes = [isNotAuthenticatedCustom]

    def post(self,request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Your password successfully reset now you can login.'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)