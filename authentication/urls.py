from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserDeviceViewSet, LoginHistoryViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'devices', UserDeviceViewSet, basename='devices')
router.register(r'login-history', LoginHistoryViewSet, basename='login-history')

urlpatterns = [
    path('', include(router.urls)),
]