from rest_framework import viewsets,status,generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from datetime import timedelta
import jwt
from .models import User,UserDevice,LoginHistory
from .serializers import (
    UserRegistrationSerializer,UserDeviceSerializer,LoginHistorySerializer,ChangePasswordSerializer
)

class AuthViewSet(viewsets.GenericViewset):
    permission_classes = [AllowAny]
    
    @action(detail = False, methods=['post'])
    def register (self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _  = Token.objects.get_or_create(user = user)
            return Response({
                'token': token.key,
                'user_id': user.id }
                            ,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.Http_400_BAD_REQUEST)
    
    @action(detail = False, methods = ['POST'])
    def login(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error':'Please provide bot username and password'}, status = status.HTTP_400_BAD_REQUEST)
            
        user = authenticate(username = username, password = password )
        
        if not user:
            self._handle_failed_login(username)
            return Response({
                'error':'invalid credentials'
            }, status = status.HTTP_401_UNAUTHORIZED)
            
        if user.account_locked_until and user.account_locked_until > timezone.now():
            return Response({
                'error':'Account is temporarily locked'
            },status = status.HTTP_403_FORBIDDEN)
            
        login(request,user)
        token, _ = Token.objects.get_or_create(user = user)
        
        
        #I will the logic for failed login attempts here
              
        