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

class AuthViewSet(viewsets.GenericViewSet):
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
        
        
        #I will write the logic for failed login attempts here
        user.failed_login_attempts = 0
        user.save()
        
        
        #Record login history
        LoginHistory.objects.create(user=user,
                                    ip_address = self._get_client_ip(request),
                                    device_info = request.META.get('HTTP_USER_AGENT',''),
                                    status = 'success'
                                    )
        return Response({
            'token':token.key,
            'user_id':user.id
        })
        
    def _handle_failed_login(self,username):
        try:
            user =User.objects.get(username = username)
            user.failed_login_attempts +=1
            
            if user.failed_login_attempts >=5:
                user.account_locked_until = timezone.now() + timedelta(minutes = 30)
                user.save()
            LoginHistory.objects.create(
                user = user,
                ip_address = self._get_client_ip(self.request),
                device_info = self.request.META.get('HTTP_USER_AGENT',''),
                status = 'failed'
            )
        except User.DoesNotExist:
            pass
            
    
    def _get_client_ip(self,request):
        x_forwarded_for = request.META.get  ('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
class UserDeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDeviceSerializer
    
    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
class LoginHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginHistorySerializer
    
    def get_queryset(self):
        return LoginHistory.objects.filter(user = self.request.user)
              
        